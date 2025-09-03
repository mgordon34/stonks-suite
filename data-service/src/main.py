import asyncio
from datetime import datetime
from typing import Any

import structlog
from fastapi import FastAPI, Query
from pydantic import BaseModel
from services.historical_data_service import HistoricalDataService

from common.config import Settings, get_settings

config: Settings = get_settings()

structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(config.log_level))
logger = structlog.get_logger(__name__)

# FastAPI app
app = FastAPI(
    title="Trading Data Service",
    description="Microservice for market data and backtesting",
    version="1.0.0",
)


# Pydantic models for API
class BacktestRequest(BaseModel):
    backtest_id: str
    user_id: str
    symbols: list[str]
    start_date: str
    end_date: str
    speed: float = 1.0
    strategy_config: dict[str, Any] = {}


@app.on_event("startup")
async def startup_event():
    try:
        logger.info(f"Starting data service in {config.environment} mode")
        logger.info(f"RABBITMQ_URL: {config.rabbitmq_url}")

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
        "environment": config.environment,
        "timestamp": asyncio.get_event_loop().time(),
    }


@app.get("/historical-data")
async def get_historical_data(start_time: datetime, end_time: datetime, timeframe: str, symbols: list[str] = Query()):
    hist_data_service = HistoricalDataService(start_time, end_time, symbols, timeframe)
    return hist_data_service.publish_historical_data()


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "status": "error",
        "message": "Internal server error",
        "detail": str(exc) if config.debug == "true" else "An error occurred",
    }
