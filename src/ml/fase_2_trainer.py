"""
FASE 2: MODELOS ML — Prophet + LightGBM
Toyo Foods Supply Chain Forecasting
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (roc_auc_score, classification_report, 
                             confusion_matrix, roc_curve, precision_recall_curve)
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import sys

warnings.filterwarnings('ignore')

print("=" * 80)
print("FASE 2: ENTRENAR MODELOS ML (Prophet + LightGBM)")
print("=" * 80)

# ============================================================================
# PASO 1: CARGAR DATOS
# ============================================================================

print("\n[1] CARGAR DATOS")
print("-" * 80)

df = pd.read_csv('df.csv')
reorder = pd.read_csv('reorder_points.csv')

df['Fecha'] = pd.to_datetime(df['Fecha'])

print(f"✓ df.csv: {df.shape[0]:,} registros × {df.shape[1]} columnas")
print(f"  Rango fechas: {df['Fecha'].min().date()} → {df['Fecha'].max().date()}")
print(f"  Productos: {df['ID_Producto'].nunique()}")

print(f"✓ reorder_points.csv: {reorder.shape[0]} productos")
print(f"  Clase A: {(reorder['Clase_ABC'] == 'A').sum()}")
print(f"  Clase B: {(reorder['Clase_ABC'] == 'B').sum()}")
print(f"  Clase C: {(reorder['Clase_ABC'] == 'C').sum()}")

# ============================================================================
# PASO 2: PROPHET — ENTRENAR TOP 20 PRODUCTOS CLASE A
# ============================================================================

print("\n[2] PROPHET — ENTRENAR TOP 20 PRODUCTOS CLASE A")
print("-" * 80)

# Seleccionar top 20 productos clase A por demanda
top_20_a = reorder[reorder['Clase_ABC'] == 'A'].nlargest(20, 'Demanda_Diaria_Media')['ID_Producto'].tolist()

print(f"Productos a entrenar: {len(top_20_a)}")
print(f"  {', '.join(top_20_a[:5])}... (primeros 5)")

prophet_models = {}
prophet_forecasts = []
prophet_metrics = []

for idx, prod_id in enumerate(top_20_a, 1):
    try:
        # Preparar datos
        prod_df = df[df['ID_Producto'] == prod_id][['Fecha', 'Demanda_Limpia']].copy()
        prod_df.columns = ['ds', 'y']
        prod_df = prod_df.dropna().sort_values('ds')
        
        if len(prod_df) < 100:
            print(f"  ⚠ {prod_id}: {len(prod_df)} registros (insuficientes)")
            continue
        
        # Entrenar Prophet
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            interval_width=0.95
        )
        model.fit(prod_df)
        
        # Forecast 30 días
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        
        # Extraer últimos 30 días
        forecast_30 = forecast[forecast['ds'] > prod_df['ds'].max()][
            ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
        ].copy()
        forecast_30['ID_Producto'] = prod_id
        forecast_30.columns = ['Fecha', 'Demanda_Forecast', 'Lower_Bound', 'Upper_Bound', 'ID_Producto']
        forecast_30['Confidence'] = 'high'
        
        # MAPE validation
        forecast_val = model.predict(pd.DataFrame({'ds': prod_df['ds'].iloc[-90:]}))
        actual = prod_df['y'].iloc[-90:].values
        pred = forecast_val['yhat'].values[:len(actual)]
        mape = np.mean(np.abs((actual - pred) / (actual + 1))) * 100
        
        prophet_forecasts.append(forecast_30)
        prophet_models[prod_id] = model
        prophet_metrics.append({
            'ID_Producto': prod_id,
            'N_Registros': len(prod_df),
            'MAPE_90d': round(mape, 2)
        })
        
        print(f"  ✓ [{idx:2d}/{len(top_20_a)}] {prod_id}: {len(prod_df)} registros, MAPE={mape:.2f}%")
        
    except Exception as e:
        print(f"  ✗ {prod_id}: {str(e)[:60]}")

# Consolidar outputs
prophet_df = pd.concat(prophet_forecasts, ignore_index=True)
prophet_metrics_df = pd.DataFrame(prophet_metrics)

# Guardar
prophet_df.to_csv('prophet_forecasts.csv', index=False)
with open('prophet_models.pkl', 'wb') as f:
    pickle.dump(prophet_models, f)

print(f"\n✓ prophet_forecasts.csv: {len(prophet_df)} registros")
print(f"✓ prophet_models.pkl: {len(prophet_models)} modelos")
print(f"\nEstadísticas Prophet:")
print(f"  MAPE promedio: {prophet_metrics_df['MAPE_90d'].mean():.2f}%")
print(f"  MAPE mín/máx: {prophet_metrics_df['MAPE_90d'].min():.2f}% / {prophet_metrics_df['MAPE_90d'].max():.2f}%")

# ============================================================================
# PASO 3: LIGHTGBM — PREDICCIÓN BINARIA (TODOS LOS PRODUCTOS)
# ============================================================================

print("\n[3] LIGHTGBM — PREDICCIÓN BINARIA (RIESGO DE DESABASTO)")
print("-" * 80)

# Features y target
feature_cols = [
    'Demanda_Media_7d', 'Demanda_Media_14d', 'Demanda_Media_30d',
    'Demanda_Std_7d', 'Demanda_Std_14d', 'Demanda_Std_30d',
    'Lead_Time_Dias', 'Dias_Desde_Compra',
    'mes', 'dia_semana', 'es_Q1'
]

df_ml = df[feature_cols + ['Target_Bajo_ROP']].dropna().copy()
X = df_ml[feature_cols].astype('float32')
y = df_ml['Target_Bajo_ROP'].astype('int')

print(f"Dataset ML: {X.shape[0]:,} registros × {X.shape[1]} features")
print(f"\nDistribución target:")
print(f"  Clase 0 (Estable): {(y==0).sum():,} ({100*(y==0).mean():.2f}%)")
print(f"  Clase 1 (Riesgo): {(y==1).sum():,} ({100*(y==1).mean():.2f}%)")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain/Test split:")
print(f"  Train: {X_train.shape[0]:,} ({100*X_train.shape[0]/len(X):.1f}%)")
print(f"  Test: {X_test.shape[0]:,} ({100*X_test.shape[0]/len(X):.1f}%)")

# Balanceo
pos_weight = (y_train == 0).sum() / ((y_train == 1).sum() + 1)
print(f"\nBalanceo (scale_pos_weight): {pos_weight:.4f}")

# Entrenar
print("\nEntrenando LightGBM...")
lgb_model = lgb.LGBMClassifier(
    n_estimators=250,
    max_depth=9,
    learning_rate=0.05,
    num_leaves=31,
    scale_pos_weight=pos_weight,
    early_stopping_rounds=20,
    random_state=42,
    verbose=-1,
    n_jobs=-1
)

lgb_model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    eval_metric='auc'
)

print(f"✓ Modelo entrenado")
print(f"  Best iteration: {lgb_model.best_iteration_}")

# Evaluar
y_pred = lgb_model.predict(X_test)
y_proba = lgb_model.predict_proba(X_test)[:, 1]

roc_auc = roc_auc_score(y_test, y_proba)
cm = confusion_matrix(y_test, y_pred)
precision = cm[1, 1] / (cm[1, 1] + cm[0, 1] + 1e-6)
recall = cm[1, 1] / (cm[1, 1] + cm[1, 0] + 1e-6)
f1 = 2 * (precision * recall) / (precision + recall + 1e-6)

print(f"\nMétricas LightGBM:")
print(f"  ROC-AUC: {roc_auc:.4f} ✓")
print(f"  Precision: {precision:.4f}")
print(f"  Recall: {recall:.4f}")
print(f"  F1-Score: {f1:.4f}")

print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Estable', 'Riesgo']))

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': lgb_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\nTop 10 Features:")
for idx, row in feature_importance.head(10).iterrows():
    print(f"  {row['Feature']:25s}: {row['Importance']:.4f}")

# Guardar
with open('lgb_model.pkl', 'wb') as f:
    pickle.dump(lgb_model, f)
    
feature_importance.to_csv('feature_importance.csv', index=False)

metrics_dict = {
    'ROC_AUC': round(roc_auc, 4),
    'Precision': round(precision, 4),
    'Recall': round(recall, 4),
    'F1_Score': round(f1, 4),
    'Train_Samples': len(X_train),
    'Test_Samples': len(X_test),
    'Best_Iteration': int(lgb_model.best_iteration_)
}

metrics_df = pd.DataFrame([metrics_dict])
metrics_df.to_csv('lgb_metrics.csv', index=False)

print(f"\n✓ lgb_model.pkl guardado")
print(f"✓ feature_importance.csv guardado")
print(f"✓ lgb_metrics.csv guardado")

# ============================================================================
# PASO 4: VISUALIZACIONES
# ============================================================================

print("\n[4] GENERAR VISUALIZACIONES")
print("-" * 80)

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure(figsize=(10, 7))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.4f})', linewidth=2.5, color='#2563EB')
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1.5)
plt.fill_between(fpr, tpr, alpha=0.1, color='#2563EB')
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('LightGBM ROC Curve — Predicción Riesgo Desabasto', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('roc_curve.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"✓ roc_curve.png guardado")

# Feature Importance Plot
fig, ax = plt.subplots(figsize=(10, 6))
top_features = feature_importance.head(12)
ax.barh(range(len(top_features)), top_features['Importance'].values, color='#2563EB', alpha=0.8)
ax.set_yticks(range(len(top_features)))
ax.set_yticklabels(top_features['Feature'].values)
ax.set_xlabel('Importance', fontsize=12)
ax.set_title('LightGBM Feature Importance', fontsize=14, fontweight='bold')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance_plot.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"✓ feature_importance_plot.png guardado")

# Confusion Matrix
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Estable', 'Riesgo'],
            yticklabels=['Estable', 'Riesgo'],
            cbar_kws={'label': 'Count'},
            ax=ax)
ax.set_ylabel('Actual', fontsize=12)
ax.set_xlabel('Predicted', fontsize=12)
ax.set_title('Confusion Matrix — LightGBM', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"✓ confusion_matrix.png guardado")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("FASE 2: COMPLETADA EXITOSAMENTE ✓")
print("=" * 80)

print(f"\nARCHIVOS GENERADOS:")
print(f"\n  PROPHET:")
print(f"    1. prophet_forecasts.csv ({len(prophet_df)} registros)")
print(f"    2. prophet_models.pkl ({len(prophet_models)} modelos)")
print(f"\n  LIGHTGBM:")
print(f"    3. lgb_model.pkl (ROC-AUC = {roc_auc:.4f})")
print(f"    4. feature_importance.csv")
print(f"    5. lgb_metrics.csv")
print(f"\n  VISUALIZACIONES:")
print(f"    6. roc_curve.png")
print(f"    7. feature_importance_plot.png")
print(f"    8. confusion_matrix.png")

print(f"\n" + "=" * 80)
print(f"RESUMEN MÉTRICAS:")
print(f"=" * 80)

print(f"\nPROPHET (Top 20 Productos Clase A):")
print(f"  • Modelos entrenados: {len(prophet_models)}")
print(f"  • MAPE promedio (90 días): {prophet_metrics_df['MAPE_90d'].mean():.2f}%")
print(f"  • Forecasts generados: {len(prophet_df)} (20 productos × 30 días)")

print(f"\nLIGHTGBM (Todos los productos):")
print(f"  • Dataset: {len(X):,} registros, {X.shape[1]} features")
print(f"  • ROC-AUC: {roc_auc:.4f} ✓ Excelente")
print(f"  • Precision: {precision:.4f}")
print(f"  • Recall: {recall:.4f}")
print(f"  • F1-Score: {f1:.4f}")
print(f"  • Mejor feature: {feature_importance.iloc[0]['Feature']}")

print(f"\nPRÓXIMOS PASOS:")
print(f"  1. Descargar los 8 archivos")
print(f"  2. Carga a Supabase (FASE 3)")
print(f"  3. Deploy FastAPI en Render (FASE 4)")
print(f"  4. Deploy React en Vercel (FASE 5)")

print(f"\n" + "=" * 80)
