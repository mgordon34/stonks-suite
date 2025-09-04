from enum import StrEnum


class MarketType(StrEnum):
    FUTURES = "Futures"
    EQUITIES = "Equities"


class FuturesProduct(StrEnum):
    NQ = "NQ"
    ES = "ES"
    YM = "YM"
    GC = "GC"


def get_market_type(symbol: str) -> MarketType:
    if symbol in FuturesProduct:
        return MarketType.FUTURES
    return MarketType.EQUITIES
