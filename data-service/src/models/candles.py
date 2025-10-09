from datetime import datetime

from database import Base
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Candle(Base):
    __tablename__ = "candles"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(index=True)
    timeframe: Mapped[str] = mapped_column(index=True)
    start_time: Mapped[datetime]
    open: Mapped[float]
    high: Mapped[float]
    low: Mapped[float]
    close: Mapped[float]
    volume: Mapped[int]

    __table_args__ = (UniqueConstraint("symbol", "timeframe", "start_time"),)
