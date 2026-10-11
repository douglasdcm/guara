from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

# ==========================================================
# ENTITIES
# ==========================================================


@dataclass
class Product:
    id: int
    name: str
    price: float
    minimum_stock: float
    stock: float = 0
    cost_price: float = 0
    sold_by_weight: bool = False


@dataclass
class Batch:
    product_id: int
    quantity: float
    expiration_date: date


@dataclass
class Customer:
    id: int
    name: str
    phone: str


@dataclass
class SaleItem:
    id: int
    sale_id: int
    product_id: int
    quantity: float
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Sale:
    id: int
    items: list[SaleItem]
    customer_id: int | None = None
    discount_percent: float = 0
    payments: dict[str, float] = field(default_factory=dict)
    delivery_address: str | None = None

    @property
    def subtotal(self) -> float:
        return sum(item.total for item in self.items)

    @property
    def total(self) -> float:
        return self.subtotal * (1 - self.discount_percent / 100)


@dataclass
class Rating:
    customer_id: int
    product_id: int
    rating: float

    def get_tuple(self):
        return (self.customer_id, self.product_id, self.rating)


@dataclass
class CashRegister:
    id: int
    opened_by: str
    initial_value: float
    opened_at: datetime = field(default_factory=datetime.now)
    closed_at: datetime | None = None
    closed: bool = True


@dataclass
class Withdrawals:
    id: int
    cash_register_id: int
    withdrawal: float


@dataclass
class User:
    id: int
    name: str
    role: str
    secret: str = None
    logged_in: bool = False

    def __repr__(self):
        return f"{self.name} | {self.role}"
