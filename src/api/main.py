from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client, Client

load_dotenv()

app = FastAPI(
    title="SupplyPredict API",
    description="Sistema de Predicción de Stockouts para Toyo Foods",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Conectado a Supabase")
except Exception as e:
    print(f"❌ Error: {e}")
    supabase = None

class Product(BaseModel):
    id_producto: str
    clase_abc: str
    demanda_diaria_media: Optional[float] = None
    lead_time_media: Optional[float] = None
    safety_stock: Optional[float] = None
    reorder_point: Optional[int] = None

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "SupplyPredict API",
        "version": "1.0.0",
        "supabase_connected": supabase is not None
    }

@app.get("/products", response_model=List[Product])
async def list_products(
    clase: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    try:
        if supabase is None:
            raise HTTPException(status_code=500, detail="Supabase no conectado")

        query = supabase.table("products").select("*")

        if clase:
            query = query.eq("clase_abc", clase)

        response = query.range(skip, skip + limit - 1).execute()
        return response.data if response.data else []

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{id_producto}", response_model=Product)
async def get_product(id_producto: str):
    try:
        if supabase is None:
            raise HTTPException(status_code=500, detail="Supabase no conectado")

        response = supabase.table("products").select("*").eq("id_producto", id_producto).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail=f"Producto no encontrado")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        if supabase is None:
            raise HTTPException(status_code=500, detail="Supabase no conectado")

        products_response = supabase.table("products").select("*", count="exact").execute()
        risk_response = supabase.table("risk_snapshot").select("*", count="exact").eq("nivel_riesgo", "Alto").execute()

        return {
            "total_productos": len(products_response.data) if products_response.data else 0,
            "productos_alto_riesgo": len(risk_response.data) if risk_response.data else 0,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
