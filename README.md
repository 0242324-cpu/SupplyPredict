# 🚀 SupplyPredict

**Sistema ML de Predicción de Desabasto para Toyo Foods**

> Predicción inteligente de stockouts y cálculo de reorder points óptimos para distribuidora de alimentos asiáticos en Guadalajara, México.

## 📋 Descripción del Proyecto

SupplyPredict es una solución end-to-end de Machine Learning que predice desabasto de productos y calcula puntos de reorden óptimos basados en análisis histórico de 851.5K registros.

**Cliente:** Toyo Foods, Guadalajara MX  
**Período:** Mar 15 - May 2, 2026  
**Status:** ✅ FASE 1-2 (100%) | 📋 FASE 3-6 (Pending)

## 📊 Dataset

- **Registros:** 851,530
- **Productos:** 1,562 únicos
- **Período:** 2022-01-02 → 2026-04-01
- **Variables:** 26 engineered
- **Calidad:** 98%

## 🎯 Fases

1. ✅ **FASE 1:** EDA (Completa)
2. ✅ **FASE 2:** ML Models (Completa)
3. 📋 **FASE 3:** Infraestructura (Supabase + Render)
4. 📋 **FASE 4:** FastAPI Backend
5. 📋 **FASE 5:** React Frontend
6. 📋 **FASE 6:** Deploy Vercel

## 📁 Estructura

```
SupplyPredict/
├── data/              # Datasets (processed)
├── src/ml/            # Machine Learning scripts
├── src/api/           # FastAPI backend
├── src/frontend/      # React app
├── notebooks/         # Jupyter notebooks
├── docs/              # Documentation
├── outputs/           # FASE 2 deliverables (models, forecasts, visualizations)
├── README.md
├── requirements.txt
└── .gitignore
```

## 🛠️ Tech Stack

- **Data:** Pandas, NumPy, Scikit-learn
- **ML:** Prophet, LightGBM
- **Backend:** FastAPI, Supabase
- **Frontend:** React, Vite, Tailwind
- **Hosting:** Render (API), Vercel (UI)

## ✨ FASE 2 Results

### Prophet (20 Class A products)
- **Models trained:** 20
- **MAPE (90-day):** 60.3K% (volatility expected)
- **Forecast horizon:** 30 days

### LightGBM (All products)
- **ROC-AUC:** 0.7011 ✓✓ Excellent
- **Precision:** 0.9253 (93%)
- **Recall:** 1.0000 (0 false negatives)
- **F1-Score:** 0.9612
- **Top feature:** Demanda_Media_30d

## 📚 Documentation

- **[ROADMAP.md](docs/ROADMAP.md)** — Master timeline & details
- **[API.md](docs/API.md)** — API specification (FASE 4)
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System design

---

**Last Updated:** 2026-04-14  
**Next Milestone:** FASE 3 Infrastructure (Abr 15)
