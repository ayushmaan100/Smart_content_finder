"""
Auth-related API routes.

This module defines a minimal APIRouter so `app.main` can include it safely.
Real implementations can provide /register, /login, /me, token issuance, etc.
"""

from fastapi import Request, HTTPException, APIRouter, Depends
import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


# Create a router instance dedicated to Auth endpoints.
router = APIRouter()

@router.get("/health")
async def auth_healthcheck():
	"""Lightweight healthcheck endpoint for the Auth router."""
	return {"status": "ok", "area": "auth"}

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = auth_header.split(" ")[1]

    resp = requests.get(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={
            "Authorization": f"Bearer {token}",
            "apikey": SUPABASE_ANON_KEY,
        },
    )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")

    return resp.json()  # contains user info



