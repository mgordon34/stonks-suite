from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: int
    timeframe: str
    start_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
