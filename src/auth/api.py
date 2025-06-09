"""Authentication API Routes - placeholder"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login():
    """Login endpoint - placeholder."""
    return {"message": "Login endpoint - not implemented"}


@router.post("/logout")
async def logout():
    """Logout endpoint - placeholder."""
    return {"message": "Logout endpoint - not implemented"} 