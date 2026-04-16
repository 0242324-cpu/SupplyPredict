from fastapi import FastAPI
import os
import sys
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = FastAPI(title="SupplyPredict API", version="1.0.0")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None
supabase_error = None

try:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(f"Missing env vars: URL={'set' if SUPABASE_URL else 'MISSING'}, KEY={'set' if SUPABASE_KEY else 'MISSING'}")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase connected", flush=True)
except Exception as e:
    supabase_error = str(e)
    print(f"❌ Supabase error: {supabase_error}", file=sys.stderr, flush=True)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "SupplyPredict API",
        "version": "1.0.0",
        "supabase_connected": supabase is not None,
        "supabase_error": supabase_error
    }

@app.get("/products")
async def list_products(skip: int = 0, limit: int = 20):
    try:
        if not supabase:
            return {"error": "Supabase not connected", "detail": supabase_error}
        response = supabase.table("products").select("*").range(skip, skip + limit - 1).execute()
        return {"data": response.data, "count": len(response.data) if response.data else 0}
    except Exception as e:
        return {"error": str(e)}

@app.get("/stats")
async def get_stats():
    try:
        if not supabase:
            return {"error": "Supabase not connected", "detail": supabase_error}
        products = supabase.table("products").select("*", count="exact").execute()
        return {"total_productos": len(products.data) if products.data else 0}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
