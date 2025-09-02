from datetime import datetime

import databento
import pandas as pd
import structlog
from models.candles import Candle

logger = structlog.get_logger(__name__)


class HistoricalDataService:
    @classmethod
    def publish_historical_data(cls, start_time: datetime, end_time: datetime, symbols: list[str], timeframe: str):
        logger.info(f"get_historical_data[{symbols}]: {start_time} - {end_time}")

        dbn_store = databento.DBNStore.from_file(path="data/glbx-mdp3-20250801-20250828.ohlcv-1m.dbn.zst")
        # dbn_store = databento.DBNStore.from_file(path="data/glbx-mdp3-20200829-20250828.ohlcv-1m.dbn.zst")

        df = dbn_store.to_df()
        logger.info(f"Retrieved {len(df)} entries in data frame")

        cls._deserialize_dbn(df, symbols, "1")

    def _deserialize_dbn(df: pd.DataFrame, symbols: list[str], timeframe: str) -> dict[str, dict[datetime, Candle]]:
        data: dict = dict.fromkeys(symbols, {})

        for index, row in df.iterrows():
            symbol: str = row.symbol[:2]

            if "-" in row.symbol or symbol not in symbols:
                continue

            if index not in data[symbol] or row.volume > data[symbol][index].volume:
                data[symbol][index] = Candle(
                    symbol, timeframe, index.to_pydatetime(), row.open, row.high, row.low, row.close, row.volume
                )

        for i in data["NQ"]:
            logger.info(f"[{i}]: {data['NQ'][i]}, {type(data['NQ'][i].start_time)}")

        return data
