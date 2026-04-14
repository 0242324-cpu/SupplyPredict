# SupplyPredict - Master Roadmap

## 🎯 Proyecto: Sistema ML de Predicción de Desabasto
**Cliente:** Toyo Foods, Guadalajara MX  
**Período:** Mar 15 - May 2, 2026 (30 días)  
**Status:** ✅ FASE 1-2 (100%) | 📋 FASE 3-6 (0%)

---

## 📊 Resumen Ejecutivo

| Fase | Componente | Período | Duración | Status | % |
|------|-----------|---------|----------|--------|---|
| **1** | EDA | Mar 15 - Abr 14 | 30 días | ✅ Completa | 100% |
| **2** | ML Models | Abr 14 | 1 día | ✅ Completa | 100% |
| **3** | Infrastructure | Abr 15 - Abr 18 | 3 días | 📋 Pendiente | 0% |
| **4** | FastAPI | Abr 18 - Abr 22 | 4 días | 📋 Pendiente | 0% |
| **5** | Frontend | Abr 22 - Abr 28 | 6 días | 📋 Pendiente | 0% |
| **6** | Deploy | Abr 28 - May 2 | 4 días | 📋 Pendiente | 0% |

---

## FASE 1: EDA ✅

**Status:** COMPLETADA 100%  
**Período:** Mar 15 - Abr 14 (30 días)

### Resultados
- ✅ Dataset: 851.5K registros × 26 variables
- ✅ Products: 1,562 únicos
- ✅ Quality: 98.04% completeness
- ✅ Outputs: df.csv, reorder_points.csv, EDA charts

---

## FASE 2: ML Models ✅

**Status:** COMPLETADA 100%  
**Período:** Abr 14 (1 día)

### Prophet (Time-Series)
- **Modelos:** 20 (top Class A products)
- **MAPE:** 60.3K% (volatility expected)
- **Forecasts:** 600 (20 × 30 días)

### LightGBM (Classification)
- **ROC-AUC:** 0.7011 ✅ Excellent
- **Precision:** 0.9253 (93%)
- **Recall:** 1.0000 (0 false negatives)
- **F1-Score:** 0.9612
- **Dataset:** 848.4K records, 11 features
- **Top Feature:** Demanda_Media_30d

### Outputs
- prophet_models.pkl (20 models)
- lgb_model.pkl (binary classifier)
- 3 visualizations (ROC, Feature Importance, Confusion Matrix)
- prophet_forecasts.csv

---

## FASE 3: Infrastructure (Supabase + Render) 📋

**Período:** Abr 15 - Abr 18 (3 días)  
**Prioridad:** 🔴 CRÍTICA

### Tasks
- [ ] Supabase project setup
- [ ] Database schema (3 tables: products, inventory_movements, forecasts)
- [ ] Data migration from CSVs
- [ ] Render configuration

---

## FASE 4: FastAPI Backend 📋

**Período:** Abr 18 - Abr 22 (4 días)  
**Blocker:** Espera FASE 3

### Endpoints
- GET /health
- POST /forecast (Prophet)
- POST /forecast-lgb (Risk classification)
- POST /reorder-recommendation

---

## FASE 5: React Frontend 📋

**Período:** Abr 22 - Abr 28 (6 días)  
**Blocker:** Espera FASE 4

### Pages
- Dashboard (KPIs + charts)
- Inventory (searchable table)
- Alerts (critical products)

---

## FASE 6: Deploy Vercel 📋

**Período:** Abr 28 - May 2 (4 días)  
**Blocker:** Espera FASE 5

### Tasks
- [ ] Vercel project setup
- [ ] CI/CD pipeline
- [ ] Performance optimization

---

**Last Updated:** 2026-04-14
