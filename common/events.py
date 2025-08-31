from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class EventType(Enum):
    MARKET_DATA = "market_data"
    SIGNAL = "signal"
    ORDER = "order"
    FILL = "fill"


class Event(ABC):
    """Base event class for all trading events."""
    
    def __init__(self, event_type: EventType, timestamp: Optional[datetime] = None):
        self.event_type = event_type
        self.timestamp = timestamp or datetime.now()
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        pass


@dataclass
class MarketEvent(Event):
    """Event representing new market data (candlestick bar)."""
    
    symbol: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    timestamp: datetime
    
    def __init__(self, symbol: str, open_price: float, high_price: float, 
                 low_price: float, close_price: float, volume: int, 
                 timestamp: Optional[datetime] = None):
        super().__init__(EventType.MARKET_DATA, timestamp)
        self.symbol = symbol
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price,
            "volume": self.volume
        }


@dataclass
class SignalEvent(Event):
    """Event representing a trading signal from a strategy."""
    
    symbol: str
    signal_type: str
    strength: float
    strategy_name: str
    timestamp: datetime
    
    def __init__(self, symbol: str, signal_type: str, strength: float, 
                 strategy_name: str, timestamp: Optional[datetime] = None):
        super().__init__(EventType.SIGNAL, timestamp)
        self.symbol = symbol
        self.signal_type = signal_type
        self.strength = strength
        self.strategy_name = strategy_name
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "signal_type": self.signal_type,
            "strength": self.strength,
            "strategy_name": self.strategy_name
        }


@dataclass
class OrderEvent(Event):
    """Event representing an order to be executed by the execution integration"""
    
    symbol: str
    order_type: str
    quantity: int
    side: str
    timestamp: datetime
    
    def __init__(
        self,
        symbol: str,
        order_type: str,
        quantity: int,
        side: str,
        timestamp: Optional[datetime] = None
    ):
        super().__init__(EventType.ORDER, timestamp)
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.side = side
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "order_type": self.order_type,
            "quantity": self.quantity,
            "side": self.side
        }


@dataclass
class FillEvent(Event):
    """Event representing a filled order from the broker."""
    
    symbol: str
    quantity: int
    side: str
    fill_price: float
    commission: float
    timestamp: datetime
    
    def __init__(self, symbol: str, quantity: int, side: str, 
                 fill_price: float, commission: float, 
                 timestamp: Optional[datetime] = None):
        super().__init__(EventType.FILL, timestamp)
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.fill_price = fill_price
        self.commission = commission
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "quantity": self.quantity,
            "side": self.side,
            "fill_price": self.fill_price,
            "commission": self.commission
        }


class EventHandler(ABC):
    @abstractmethod
    def handle_event(self, event: Event) -> None:
        """Handle an incoming event."""
        pass


class EventBus:
    def __init__(self):
        self._handlers: Dict[EventType, list[EventHandler]] = {}
    
    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Subscribe a handler to a specific event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def publish(self, event: Event) -> None:
        """Publish an event to all subscribed handlers."""
        if event.event_type in self._handlers:
            for handler in self._handlers[event.event_type]:
                handler.handle_event(event)

