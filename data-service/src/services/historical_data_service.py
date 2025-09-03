from dataclasses import dataclass
from datetime import datetime

import databento
import pandas as pd
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

        dbn_store = databento.DBNStore.from_file(path="data/glbx-mdp3-20250801-20250828.ohlcv-1m.dbn.zst")
        # dbn_store = databento.DBNStore.from_file(path="data/glbx-mdp3-20200829-20250828.ohlcv-1m.dbn.zst")

        df = dbn_store.to_df()
        logger.info(f"Retrieved {len(df)} entries in data frame")

        return self._deserialize_dbn(df)

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
