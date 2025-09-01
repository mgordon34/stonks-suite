from datetime import datetime

import databento
import pytz
import structlog

logger = structlog.get_logger(__name__)


class HistoricalDataService:
    @classmethod
    def publish_historical_data(
        cls, start_time: datetime, end_time: datetime, symbols: list[str]
    ):
        logger.info(f"get_historical_data[{symbols}]: {start_time} - {end_time}")

        dbn_store = databento.DBNStore.from_file(
            path="data/glbx-mdp3-20250801-20250828.ohlcv-1m.dbn.zst"
        )

        df = dbn_store.to_df()
        logger.info(f"Retrieved {len(df)} entries in data frame")

        # Times are in UTC
        for index, _row in df.head(5).iterrows():
            logger.info(
                f"Index: {index}: vs "
                f"{start_time.astimezone(pytz.utc)} = {index > start_time}"
            )
