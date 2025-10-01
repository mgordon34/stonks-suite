import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import databento
import pandas as pd
import pytz
import structlog
from models.candles import Candle

logger = structlog.get_logger(__name__)


@dataclass
class HistoricalDataService:
    start_time: datetime
    end_time: datetime
    symbols: list[str]
    timeframe: str

    def __post_init__(self):
        self.curr_dbn_file: Optional[databento.DBNStore] = None

    def publish_historical_data(self) -> dict[str, dict[datetime, Candle]]:
        logger.info(f"get_historical_data[{self.symbols}]: {self.start_time} - {self.end_time}")

        curr_date: datetime.date = self.start_time.astimezone(pytz.utc).date()
        end_date: datetime.date = self.end_time.astimezone(pytz.utc).date()
        while curr_date <= end_date:
            logger.debug(f"Getting db for {curr_date}")

            dbn_store = self.get_dbn_for_date(curr_date)
            df = dbn_store.to_df()
            logger.info(f"Retrieved {len(df)} entries in data frame")
            logger.info(self._deserialize_dbn(df))

            curr_date += timedelta(days=1)

        return "OK"

    def get_dbn_for_date(self, date: datetime.date) -> databento.DBNStore:
        logger.debug(f"Finding dbn store for {date}")

        for dbn_path in os.listdir("data"):
            if _date_in_dbn_str(date, dbn_path):
                logger.debug(f"{date} in {dbn_path}")
                return databento.DBNStore.from_file(path="data/" + dbn_path)

    def _deserialize_dbn(self, df: pd.DataFrame) -> dict[str, dict[datetime, Candle]]:
        data: dict = {s: {} for s in self.symbols}

        for index, row in df.iterrows():
            symbol: str = row.symbol[:2]

            if "-" in row.symbol or symbol not in self.symbols:
                continue

            if index not in data[symbol] or row.volume > data[symbol][index].volume:
                data[symbol][index] = Candle(
                    symbol, self.timeframe, index.to_pydatetime(), row.open, row.high, row.low, row.close, row.volume
                )

        return data


def _date_in_dbn_str(date: datetime.date, dbn_path: str) -> bool:
    if "ohlc" not in dbn_path:
        return False

    dbn_words = dbn_path.split("/")[-1].split(".")[0].split("-")
    date_format = "%Y%m%d"
    start_date = datetime.strptime(dbn_words[2], date_format).date()
    end_date = datetime.strptime(dbn_words[3], date_format).date()

    return start_date <= date <= end_date
