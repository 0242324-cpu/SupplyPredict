# 🚀 FASE 3 - SupplyPredict Complete Setup Guide

## 📋 Overview

FASE 3 configura la infraestructura cloud completa:
- **Supabase:** Base de datos PostgreSQL con 3 tablas (products, forecasts, inventory_movements)
- **Render:** Web Service hosting para FastAPI
- **CSV Migration:** Cargar datos de FASE 1-2 a Supabase

**Total Time:** 30-45 minutos  
**Cost:** $0 (free tiers)  
**Prerequisites:** Email para Supabase, Email para Render

---

## 📁 PASO 1: DESCARGA LOS ARCHIVOS NECESARIOS

### Archivo 1: reorder_points.csv (1,562 registros)
```bash
curl -o ~/SupplyPredict/data/processed/reorder_points.csv \
  https://github.com/0242324-cpu/SupplyPredict/raw/main/data/processed/reorder_points.csv
```

**Campos:** ID_Producto, Clase_ABC, Demanda_Diaria_Est, Lead_Time_Media, Safety_Stock, Reorder_Point

### Archivo 2: prophet_forecasts.csv (600 registros)
```bash
curl -o ~/SupplyPredict/outputs/prophet_forecasts.csv \
  https://github.com/0242324-cpu/SupplyPredict/raw/main/outputs/prophet_forecasts.csv
```

**Campos:** id_producto, ds, yhat, yhat_lower, yhat_upper

---

## 🎯 PASO 2: CREAR PROYECTO SUPABASE

1. **Signup:** https://supabase.com
2. **New Project**
   - Name: `SupplyPredict`
   - Region: `us-east-1` (o más cercana)
   - Database Password: Crea una fuerte (guárdala)
3. Espera a que inicialice (~5 min)
4. **Copia credenciales** de Settings → API:
   - PROJECT_URL
   - ANON_PUBLIC_KEY
   - SERVICE_ROLE_SECRET

---

## 🎯 PASO 3: CREAR SCHEMA SQL

En Supabase → Database → SQL Editor → New Query

Ejecuta este SQL (cópialo completo):

```sql
-- TABLA 1: PRODUCTS
CREATE TABLE products (
  id_producto TEXT PRIMARY KEY,
  clase_abc CHAR(1),
  demanda_diaria_media NUMERIC(12,4),
  lead_time_media NUMERIC(8,2),
  safety_stock NUMERIC(12,4),
  reorder_point INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_products_clase ON products(clase_abc);

-- TABLA 2: FORECASTS
CREATE TABLE forecasts (
  id_producto TEXT REFERENCES products(id_producto) ON DELETE CASCADE,
  fecha DATE,
  demanda_forecast NUMERIC(12,2),
  lower_bound NUMERIC(12,2),
  upper_bound NUMERIC(12,2),
  model_version TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (id_producto, fecha)
);
CREATE INDEX idx_forecasts_producto ON forecasts(id_producto);
CREATE INDEX idx_forecasts_fecha ON forecasts(fecha);

-- TABLA 3: INVENTORY_MOVEMENTS
CREATE TABLE inventory_movements (
  fecha DATE,
  id_producto TEXT REFERENCES products(id_producto) ON DELETE CASCADE,
  stock_disponible INTEGER,
  stock_minimo INTEGER,
  demanda_implicita NUMERIC(12,2),
  demanda_limpia NUMERIC(12,2),
  cantidad_comprada INTEGER,
  venta_total NUMERIC(14,2),
  demanda_media_7d NUMERIC(12,4),
  demanda_media_14d NUMERIC(12,4),
  demanda_media_30d NUMERIC(12,4),
  demanda_std_7d NUMERIC(12,4),
  demanda_std_14d NUMERIC(12,4),
  demanda_std_30d NUMERIC(12,4),
  lead_time_dias INTEGER,
  dias_desde_compra INTEGER,
  mes INTEGER,
  dia_semana INTEGER,
  es_q1 BOOLEAN,
  target_bajo_rop BOOLEAN,
  PRIMARY KEY (fecha, id_producto)
);
CREATE INDEX idx_inv_fecha ON inventory_movements(fecha);
CREATE INDEX idx_inv_producto ON inventory_movements(id_producto);
```

---

## 🎯 PASO 4: CARGAR DATOS CSV

### 4a. Tabla PRODUCTS
1. Database → Tables → **products**
2. Click **Import data**
3. Selecciona: `reorder_points.csv`
4. **Column Mapping:**
   ```
   ID_Producto        → id_producto
   Clase_ABC          → clase_abc
   Demanda_Diaria_Est → demanda_diaria_media
   Lead_Time_Media    → lead_time_media
   Safety_Stock       → safety_stock
   Reorder_Point      → reorder_point
   ```
5. Click **Import**
6. ✅ Deberías ver: "1,562 rows inserted"

### 4b. Tabla FORECASTS
1. Database → Tables → **forecasts**
2. Click **Import data**
3. Selecciona: `prophet_forecasts.csv`
4. **Column Mapping:**
   ```
   id_producto → id_producto
   ds          → fecha
   yhat        → demanda_forecast
   yhat_lower  → lower_bound
   yhat_upper  → upper_bound
   ```
5. Click **Import**
6. ✅ Deberías ver: "600 rows inserted"

---

## 🎯 PASO 5: CONFIGURAR RLS (Row Level Security)

Para cada tabla (products, forecasts, inventory_movements):

1. Database → Tables → [tabla]
2. Click "RLS" (escudito)
3. **New policy**
   - Name: `allow_public_read`
   - Permissions: SELECT ✓
   - For: USING
   - Expression: `(true)`
   - Roles: anon ✓, authenticated ✓
4. **Save**

---

## 🎯 PASO 6: CREAR WEB SERVICE EN RENDER

1. **Signup:** https://render.com (usa GitHub)
2. **New+ → Web Service**
3. **Connect Repository:** `0242324-cpu/SupplyPredict`
4. **Configure:**
   - Name: `SupplyPredict-API`
   - Environment: Python 3.9
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables:**
   ```
   SUPABASE_URL=[tu-project-url]
   SUPABASE_KEY=[tu-anon-key]
   SUPABASE_SERVICE_ROLE_KEY=[tu-service-role-key]
   ```
6. **Create Web Service**
7. ⏳ Espera 2-3 minutos
8. ✅ Guarda la URL cuando aparezca

---

## 🎯 PASO 7: CREAR .env LOCAL

En `~/SupplyPredict/.env`:

```env
SUPABASE_URL=https://[proyecto-id].supabase.co
SUPABASE_KEY=[tu-anon-public-key]
SUPABASE_SERVICE_ROLE_KEY=[tu-service-role-secret]
SUPABASE_DB_PASSWORD=[contraseña-db]
RENDER_API_URL=https://[tu-app].onrender.com
API_PORT=8000
API_HOST=0.0.0.0
ENVIRONMENT=production
```

---

## ✅ VERIFICACIÓN

En Supabase SQL Editor:
```sql
SELECT COUNT(*) FROM products;    -- debe ser 1562
SELECT COUNT(*) FROM forecasts;   -- debe ser 600
```

---

## 📊 Resultado Final

✅ Supabase project con 3 tablas y datos cargados  
✅ Render Web Service con API URL  
✅ Credenciales en `.env` local  
✅ RLS policies configuradas  

**FASE 3 COMPLETA** 🎉

---

**Tiempo:** 30-45 minutos  
**Próximo:** FASE 4 - FastAPI Backend  
**Status:** Ready to deploy
