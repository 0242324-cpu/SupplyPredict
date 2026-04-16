from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI
app = FastAPI(
    title="SupplyPredict API",
    description="Sistema de Predicción de Stockouts para Toyo Foods",
    version="1.0.0"
)

# CORS para permitir acceso desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar a Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Conectado a Supabase exitosamente")
except Exception as e:
    print(f"❌ Error conectando a Supabase: {e}")
    supabase = None

# ==================== SCHEMAS PYDANTIC ====================

class Product(BaseModel):
    id_producto: str
    clase_abc: str
    demanda_diaria_media: Optional[float] = None
    lead_time_media: Optional[float] = None
    safety_stock: Optional[float] = None
    reorder_point: Optional[int] = None

class Forecast(BaseModel):
    id_producto: str
    fecha: str
    demanda_forecast: Optional[float] = None
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None
    confidence: Optional[str] = None

class RiskSnapshot(BaseModel):
    id_producto: str
    stock_disponible: Optional[int] = None
    reorder_point: Optional[int] = None
    riesgo_proba: Optional[float] = None
    riesgo_pred: Optional[int] = None
    nivel_riesgo: Optional[str] = None

# ==================== ENDPOINTS ====================

@app.get("/health", tags=["Health"])
async def health_check():
    """Verificar que la API está activa"""
    return {
        "status": "ok",
        "service": "SupplyPredict API",
        "version": "1.0.0",
        "supabase_connected": supabase is not None
    }

@app.get("/products", tags=["Products"], response_model=List[Product])
async def list_products(
    clase: Optional[str] = Query(None, description="Filtrar por clase (A, B, C)"),
    skip: int = Query(0, ge=0, description="Saltar N registros"),
    limit: int = Query(20, ge=1, le=100, description="Límite de registros")
):
    """
    Listar todos los productos con filtros opcionales

    - **clase**: Filtrar por clase ABC (A, B, C)
    - **skip**: Paginación - saltar registros
    - **limit**: Paginación - cantidad de registros
    """
    try:
        if supabase is None:
            raise HTTPException(status_code=500, detail="Supabase no conectado")

        query = supabase.table("products").select("*")

        if clase:
            query = query.eq("clase_abc", clase)

        response = query.range(skip, skip + limit - 1).execute()

        if response.data:
            return response.data
        return []

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando productos: {str(e)}")

@app.get("/products/{id_producto}", tags=["Products"], response_model=Product)
async def get_product(id_producto: str):
    """
    Obtener detalle de un producto específico
    """
    try:
        if supabase is None:
            raise HTTPException(status_code=500, detail="Supabase no conectado")

        response = supabase.table("products").select("*").eq("id_producto", id_producto).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail=f"Producto {id_producto} no encontrado")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando producto: {str(e)}")

@app.get("/forecasts/{id_producto}", tags=["Forecasts"], response_model=List[Forecast])
async def get_forecasts(id_producto: str):
    """
    Obtener predicciones de demanda (30 días) para un producto
    """
    try:
        if supabase is None:
            raise HTTPException(status_code=500, detail="Supabase no conectado")

        response = supabase.table("forecasts").select("*").eq("id_producto", id_producto).order("fecha").execute()

        if not response.data:
            raise HTTPException(status_code=404, detail=f"No hay forecasts para {id_producto}")

        return response.data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando forecasts: {str(e)}")

@app.get("/risk-snapshot", tags=["Risk"], response_model=List[RiskSnapshot])
async def get_risk_snapshot(
    nivel_riesgo: Optional[str] = Query(None, description="Filtrar por nivel (Alto, Medio, Bajo)"),
    top_n: int = Query(20, ge=1, le=100, description="Top N productos en riesgo")
):
    """
    Obtener snapshot de productos en riesgo de stockout

    - **nivel_riesgo**: Filtrar por nivel de riesgo
    - **top_n**: Cantidad de productos a devolver
    """
    try:
        if supabase is None:
            raise HTTPException(status_code=500, detail="Supabase no conectado")

        query = supabase.table("risk_snapshot").select("*").order("riesgo_proba", desc=True).limit(top_n)

        if nivel_riesgo:
            query = query.eq("nivel_riesgo", nivel_riesgo)

        response = query.execute()

        if not response.data:
            return []

        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando riesgos: {str(e)}")

@app.get("/stats", tags=["Analytics"])
async def get_stats():
    """
    Obtener estadísticas generales del sistema
    """
    try:
        if supabase is None:
            raise HTTPException(status_code=500, detail="Supabase no conectado")

        products_response = supabase.table("products").select("*", count="exact").execute()
        risk_response = supabase.table("risk_snapshot").select("*", count="exact").eq("nivel_riesgo", "Alto").execute()
        forecasts_response = supabase.table("forecasts").select("*", count="exact").execute()

        return {
            "total_productos": len(products_response.data) if products_response.data else 0,
            "productos_alto_riesgo": len(risk_response.data) if risk_response.data else 0,
            "total_forecasts": len(forecasts_response.data) if forecasts_response.data else 0,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando estadísticas: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
