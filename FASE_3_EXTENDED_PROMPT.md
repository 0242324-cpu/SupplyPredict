# 🚀 FASE 3 Extended Prompt para Claude Code

## 📋 INTRODUCCIÓN

Copia ESTE TEXTO COMPLETO en Claude Code y sigue los pasos.

Este prompt te guiará a través de 7 tareas para completar FASE 3:
- Supabase cloud database setup
- PostgreSQL schema creation
- CSV data migration
- Row Level Security policies
- Render Web Service deployment
- Environment configuration

**Tiempo estimado:** 30-45 minutos  
**Costo:** $0 (free tiers)

---

## 📋 ANTES DE EMPEZAR

✅ Tienes descargados estos 2 archivos:
- `reorder_points.csv` en ~/SupplyPredict/data/processed/
- `prophet_forecasts.csv` en ~/SupplyPredict/outputs/

✅ Tienes listos:
- Email para Supabase
- Email para Render  
- Navegador abierto

---

## 🎯 TAREA 1: SUPABASE PROJECT

### 1.1 Signup
1. Ve a https://supabase.com
2. Click "Start your project"
3. Sign up con tu email o GitHub

### 1.2 Crear Proyecto
1. Click "New project"
2. **Name:** SupplyPredict
3. **Region:** us-east-1 (o la más cercana)
4. **Database Password:** Crea una fuerte (ej: Sup1y@Pred1ct2026!)
5. Click "Create new project"
6. Espera 5 minutos a que inicialice

### 1.3 Guardar Credenciales
Cuando esté listo, ve a **Settings → API**

Copia TRES valores:
1. Project URL (ej: https://abc123.supabase.co)
2. Anon Public Key (empieza con eyJ...)
3. Service Role Secret (también empieza con eyJ...)

Guarda estos en un block de notas. Los necesitarás después.

---

## 🎯 TAREA 2: SQL SCHEMA

En Supabase → Database → SQL Editor → New Query

Copia TODO este SQL y pégalo:

```sql
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

Click **Execute**

✅ Deberías ver 3 tablas en Database → Tables

---

## 🎯 TAREA 3: CARGAR CSV - PARTE A (products)

1. Database → Tables → **products**
2. Click **"Import data"** (arriba a la derecha)
3. Selecciona: `reorder_points.csv`
4. Espera a que cargue

**COLUMN MAPPING (muy importante):**
Haz click en cada header y selecciona la columna correcta de la tabla:

| CSV Column | Table Column |
|-----------|--------------|
| ID_Producto | id_producto |
| Clase_ABC | clase_abc |
| Demanda_Diaria_Est | demanda_diaria_media |
| Lead_Time_Media | lead_time_media |
| Safety_Stock | safety_stock |
| Reorder_Point | reorder_point |

5. Click **Import**
6. ✅ Deberías ver: "1,562 rows inserted"

---

## 🎯 TAREA 3: CARGAR CSV - PARTE B (forecasts)

1. Database → Tables → **forecasts**
2. Click **"Import data"**
3. Selecciona: `prophet_forecasts.csv`

**COLUMN MAPPING:**

| CSV Column | Table Column |
|-----------|--------------|
| id_producto | id_producto |
| ds | fecha |
| yhat | demanda_forecast |
| yhat_lower | lower_bound |
| yhat_upper | upper_bound |

5. Click **Import**
6. ✅ Deberías ver: "600 rows inserted"

---

## 🎯 TAREA 4: RLS POLICIES

Para cada tabla (products, forecasts, inventory_movements):

1. Database → Tables → [tabla]
2. Click el ícono "RLS" (escudito)
3. Click **"New policy"**
4. Completa así:
   - **Name:** allow_public_read
   - **Permissions:** SELECT ✓
   - **For:** USING
   - **Expression:** (true)
   - **Roles:** anon ✓, authenticated ✓
5. Click **Review** → **Save policy**

Repite para las 3 tablas.

---

## 🎯 TAREA 5: RENDER WEB SERVICE

### 5.1 Signup
1. Ve a https://render.com
2. Click "Get started" o "Sign up"
3. Usa GitHub account (recomendado)
4. Autoriza Render a acceder a GitHub

### 5.2 Crear Web Service
1. Dashboard → **New+** → **Web Service**
2. Click **"Connect a repository"**
3. Busca: `0242324-cpu/SupplyPredict`
4. Selecciona y click **Continue**

### 5.3 Configurar
Completa estos campos:

- **Name:** SupplyPredict-API
- **Environment:** Python 3.9
- **Region:** Default (USA)
- **Branch:** main

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

**Plan:** Free (abajo)

### 5.4 Environment Variables
Scroll down y busca **"Environment"**

Click **"Add Environment Variable"** y agrega estos 3:

```
SUPABASE_URL = https://[tu-project-id].supabase.co
SUPABASE_KEY = [tu-anon-public-key]
SUPABASE_SERVICE_ROLE_KEY = [tu-service-role-secret]
```

(Usa los valores que guardaste en TAREA 1.3)

### 5.5 Deploy
Click **"Create Web Service"**

Espera 2-3 minutos. Cuando veas "Deploy successful" y una URL como:
```
https://supplypredict-api.onrender.com
```

✅ **Guarda esta URL. La necesitarás en TAREA 6.**

---

## 🎯 TAREA 6: CREAR .env LOCAL

En tu terminal (CLI de Claude Code):

```bash
cat > ~/.env << 'ENVFILE'
SUPABASE_URL=https://[tu-project-id].supabase.co
SUPABASE_KEY=[tu-anon-public-key]
SUPABASE_SERVICE_ROLE_KEY=[tu-service-role-secret]
SUPABASE_DB_PASSWORD=[la-contraseña-de-db-que-creaste]
RENDER_API_URL=https://[tu-app].onrender.com
API_PORT=8000
API_HOST=0.0.0.0
ENVIRONMENT=production
ENVFILE
```

O manualmente:
```bash
nano ~/SupplyPredict/.env
```
Y pega el contenido arriba.

---

## 🎯 TAREA 7: VERIFICACIÓN

En Supabase → Database → SQL Editor

Ejecuta:
```sql
SELECT COUNT(*) as total_products FROM products;
```

Deberías ver: **1562**

Ejecuta:
```sql
SELECT COUNT(*) as total_forecasts FROM forecasts;
```

Deberías ver: **600**

---

## ✅ COMPLETASTE FASE 3!

¡Felicidades! Ahora tienes:

✅ Supabase project con 3 tablas  
✅ 1,562 productos cargados  
✅ 600 forecasts cargados  
✅ RLS policies configuradas  
✅ Render Web Service deployado  
✅ Variables de entorno guardadas  

---

## 📊 Credenciales Guardadas

Deberías tener guardados estos 5 valores (en .env):
1. SUPABASE_URL
2. SUPABASE_KEY
3. SUPABASE_SERVICE_ROLE_KEY
4. RENDER_API_URL
5. DATABASE_PASSWORD

Estos son CRÍTICOS para FASE 4.

---

## 🎯 PRÓXIMO PASO

FASE 4: FastAPI Backend
- Crear 4 endpoints
- Conectar a Supabase
- Deploy en Render

Tiempo estimado: 4 días (Abr 18-22)

---

**Status:** FASE 3 COMPLETA  
**Complexity:** Medium (pero todas las instrucciones están aquí)  
**Time spent:** 30-45 minutos  
**Next:** FASE 4 - FastAPI Backend

🚀 **¡Buen trabajo!**
