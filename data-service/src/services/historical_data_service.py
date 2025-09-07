import os
from dataclasses import dataclass
from datetime import datetime, timedelta

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

    def publish_historical_data(self) -> dict[str, dict[datetime, Candle]]:
        logger.info(f"get_historical_data[{self.symbols}]: {self.start_time} - {self.end_time}")

        # data: dict = {s: {} for s in self.symbols}

        for symbol in self.symbols:
            df = self.get_db_data(symbol)
            dbn_store = databento.DBNStore.from_file(path="data/glbx-mdp3-20250801-20250828.ohlcv-1m.dbn.zst")
            # dbn_store = databento.DBNStore.from_file(path="data/glbx-mdp3-20200829-20250828.ohlcv-1m.dbn.zst")

        df = dbn_store.to_df()
        logger.info(f"Retrieved {len(df)} entries in data frame")

        return self._deserialize_dbn(df)

    def get_db_data(self, symbol: str) -> pd.DataFrame:
        curr_date: datetime.date = self.start_time.astimezone(pytz.utc).date()
        end_date: datetime.date = self.end_time.astimezone(pytz.utc).date()
        dbns: list[str] = os.listdir("data")
        logger.debug(f"data dir: {dbns}")
        while curr_date <= end_date:
            logger.debug(f"Getting db for {curr_date}")

            curr_date += timedelta(days=1)

    def get_dbn_for_date(date: datetime.date) -> databento.DBNStore:
        logger.debug(f"Finding dbn store for {date}")

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
