from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.db import mostrar_ultima, mostrar_por_fecha, mostrar_rango, health_check
from typing import Optional
from datetime import datetime
import time

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

# FastAPI app
app = FastAPI(
    title="BCV Exchange Rate API",
    description="Venezuelan Central Bank (BCV) official exchange rates - Community API 🇻🇪",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware (allow all origins for public API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory cache
cache = {"latest": None, "timestamp": 0}
CACHE_TTL = 3600  # 1 hour

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "name": "BCV Exchange Rate API",
        "version": "2.0.0",
        "description": "Free community API for Venezuelan exchange rates",
        "docs": "/docs",
        "endpoints": {
            "latest": "/api/tasa",
            "by_date": "/api/tasa?fecha=YYYY-MM-DD",
            "range": "/api/tasa/rango?desde=YYYY-MM-DD&hasta=YYYY-MM-DD"
        },
        "rate_limit": "100 requests/hour per IP",
        "source": "https://github.com/yourname/tasa-bcv"
    }

@app.get("/health")
def health():
    """Health check endpoint for Cloud Run"""
    db_health = health_check()
    return {
        "status": "healthy" if db_health.get("status") == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_health
    }

@app.get("/api/tasa")
@limiter.limit("100/hour")
def get_rate(
    request: Request,
    fecha: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date in YYYY-MM-DD format")
):
    """
    Get exchange rate for a specific date or the latest rate.
    
    - **fecha**: Optional date in YYYY-MM-DD format
    - If no date provided, returns the latest rate
    - Rate limited to 100 requests/hour per IP
    """
    try:
        if not fecha:
            # Check cache for latest rate
            current_time = time.time()
            if cache["latest"] and (current_time - cache["timestamp"]) < CACHE_TTL:
                return cache["latest"]
            
            tasa = mostrar_ultima()
            if tasa:
                # Update cache
                cache["latest"] = tasa
                cache["timestamp"] = current_time
        else:
            tasa = mostrar_por_fecha(fecha)
        
        if not tasa:
            raise HTTPException(
                status_code=404,
                detail=f"No rate found for {fecha or 'today'}. Data might not be available yet."
            )
        
        return tasa
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/tasa/rango")
@limiter.limit("100/hour")
def get_range(
    request: Request,
    desde: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Start date (YYYY-MM-DD)"),
    hasta: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="End date (YYYY-MM-DD)")
):
    """
    Get exchange rates for a date range.
    
    - **desde**: Start date in YYYY-MM-DD format (required)
    - **hasta**: End date in YYYY-MM-DD format (required)
    - Returns array of rates ordered by date
    - Rate limited to 100 requests/hour per IP
    """
    try:
        # Validate date order
        if desde > hasta:
            raise HTTPException(
                status_code=400,
                detail="Start date (desde) must be before end date (hasta)"
            )
        
        tasas = mostrar_rango(desde, hasta)
        
        if not tasas:
            raise HTTPException(
                status_code=404,
                detail=f"No rates found between {desde} and {hasta}"
            )
        
        return tasas
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/metrics")
def metrics():
    """Simple metrics endpoint"""
    try:
        db_health = health_check()
        return {
            "total_records": db_health.get("records", 0),
            "cache_status": "active" if cache["latest"] else "cold",
            "last_cached": datetime.fromtimestamp(cache["timestamp"]).isoformat() if cache["timestamp"] else None
        }
    except Exception as e:
        return {"error": str(e)}
