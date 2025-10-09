from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CandleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    timeframe: str
    start_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class CandleCreate(CandleBase):
    pass


class Candle(CandleBase):
    id: int

    class Config:
        orm_mode = True
