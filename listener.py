# listener.py (ajoute à ton repo)
from fastapi import FastAPI, Request, HTTPException
from supabase import create_client
import os
import hmac
import hashlib

app = FastAPI()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

@app.post("/payhip-webhook")
async def payhip_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("payhip-signature")  # Si Payhip l'envoie
    
    # Vérifie signature (optionnel, à implémenter selon docs Payhip)
    
    data = await request.json()
    
    email = data.get("customer", {}).get("email")
    event = data.get("event")  # "paid", "subscription.created", etc.
    payhip_id = data.get("payhip_id")
    
    if not email:
        raise HTTPException(status_code=400, detail="No email")
    
    # Upsert dans Supabase
    status = "active" if event in ["paid", "subscription.created"] else "cancelled"
    
    supabase.table("customers").upsert({
        "email": email,
        "payhip_id": payhip_id,
        "subscription_status": status,
        "updated_at": "now()"
    }).execute()
    
    return {"status": "ok"}
