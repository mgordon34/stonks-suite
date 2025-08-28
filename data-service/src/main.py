import os
import asyncio
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Trading Data Service",
    description="Microservice for market data and backtesting",
    version="1.0.0"
)

# Pydantic models for API
class BacktestRequest(BaseModel):
    backtest_id: str
    user_id: str
    symbols: list[str]
    start_date: str
    end_date: str
    speed: float = 1.0
    strategy_config: Dict[str, Any] = {}

@app.on_event("startup")
async def startup_event():
    try:
        # Get environment variables
        rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://localhost:5672')
        env = os.getenv('ENV', 'development')
        
        logger.info(f"Starting data service in {env} mode")
        logger.info(f"RABBITMQ_URL: {rabbitmq_url}")
        
    except Exception as e:
        logger.error(f"Failed to initialize data service: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down data service...")
    

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "data-service",
        "environment": os.getenv('ENV', 'development'),
        "timestamp": asyncio.get_event_loop().time()
    }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "status": "error",
        "message": "Internal server error",
        "detail": str(exc) if os.getenv('DEBUG', 'false').lower() == 'true' else "An error occurred"
    }

# Main entry point
if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8001))
    reload = os.getenv('HOT_RELOAD', 'false').lower() == 'true'
    
    logger.info(f"Starting data service on {host}:{port}")
    logger.info(f"Hot reload: {reload}")
    
    # Start the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=os.getenv('LOG_LEVEL', 'info').lower()
    )
