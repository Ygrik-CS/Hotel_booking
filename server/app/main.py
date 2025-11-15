"""FastAPI application main entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import init_db
from middleware.cors import CORS_SETTINGS
from routers import (
    auth_router,
    hotel_router,
    search_router,
    cart_router,
    booking_router,
    payment_router
)
from core.frp import event_bus, log_event
from config.settings import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Hotel Booking System with Functional Programming",
    version="1.0.0",
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    **CORS_SETTINGS
)

# Include routers
app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(search_router)
app.include_router(cart_router)
app.include_router(booking_router)
app.include_router(payment_router)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    # Static directory might not exist yet
    pass


@app.on_event("startup")
async def startup_event():
    """Initialize database and event bus on startup."""
    init_db()
    # Subscribe to events for logging
    event_bus.subscribe("SEARCH", log_event)
    event_bus.subscribe("BOOKED", log_event)
    event_bus.subscribe("CANCELLED", log_event)
    event_bus.subscribe("PAYMENT", log_event)
    print(f"✅ {settings.APP_NAME} started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    event_bus.clear()
    print("👋 Application shutdown")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Hotel Booking System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
