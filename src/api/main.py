from fastapi import FastAPI
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = FastAPI(title="SupplyPredict API", version="1.0.0")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase connected")
except Exception as e:
    print(f"❌ Error: {e}")
    supabase = None

@app.get("/health")
async def health():
    return {"status": "ok", "service": "SupplyPredict API", "version": "1.0.0"}

@app.get("/products")
async def list_products(skip: int = 0, limit: int = 20):
    try:
        if not supabase:
            return {"error": "Supabase not connected"}
        response = supabase.table("products").select("*").range(skip, skip + limit - 1).execute()
        return {"data": response.data, "count": len(response.data) if response.data else 0}
    except Exception as e:
        return {"error": str(e)}

@app.get("/stats")
async def get_stats():
    try:
        if not supabase:
            return {"error": "Supabase not connected"}
        products = supabase.table("products").select("*", count="exact").execute()
        return {"total_productos": len(products.data) if products.data else 0}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
