from datetime import datetime

import databento
import pandas as pd
import structlog
from models.candles import Candle

logger = structlog.get_logger(__name__)


class HistoricalDataService:
    @classmethod
    def publish_historical_data(cls, start_time: datetime, end_time: datetime, symbols: list[str]):
        logger.info(f"get_historical_data[{symbols}]: {start_time} - {end_time}")

        dbn_store = databento.DBNStore.from_file(path="data/glbx-mdp3-20250801-20250828.ohlcv-1m.dbn.zst")
        # dbn_store = databento.DBNStore.from_file(path="data/glbx-mdp3-20200829-20250828.ohlcv-1m.dbn.zst")

        df = dbn_store.to_df()
        logger.info(f"Retrieved {len(df)} entries in data frame")

        cls._deserialize_dbn(symbols, df)

    def _deserialize_dbn(symbols: list[str], df: pd.DataFrame) -> dict[str, dict[datetime, Candle]]:
        # Times are in UTC
        bars = {
            "NQ": {},
            "ES": {},
        }
        for index, row in df.head(100000).iterrows():
            # logger.info(
            #     f"Index: {index}: vs "
            #     f"{start_time.astimezone(pytz.utc)} = {index > start_time}"
            # )
            if "-" in row.symbol:
                continue
            symbol = row.symbol[:2]

            logger.info(f"[{symbol}]: {index}, volume: {row.volume}")
            if index not in bars[symbol] or row.volume > bars[symbol][index].volume:
                bars[symbol][index] = row

        for i in bars["NQ"]:
            logger.info(f"[{i}]: {bars['NQ'][i]}")
