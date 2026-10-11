from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String

from bakery.backend.database import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float)
    stock = Column(Float, default=0)
    minimum_stock = Column(Float, default=0)
    sold_by_weight = Column(Boolean, default=False)


class RatingModel(Base):
    __tablename__ = "ratings"

    customer_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    rating = Column(Float)


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(String)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    role = Column(String)
    secret = Column(String)
    logged_in = Column(Boolean, default=False)


class SaleModel(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(Float)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    delivery_address = Column(String)


class SaleItemModel(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    quantity = Column(Float)
    unit_price = Column(Float)
    total = Column(Float)


class BatchModel(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    expiration_date = Column(Date)


class CashRegisterModel(Base):
    __tablename__ = "cash_register"

    id = Column(Integer, primary_key=True, autoincrement=True)
    opened_by = Column(String)
    opened_at = Column(Date)
    closed_at = Column(Date)
    initial_value = Column(Float)
    closed = Column(Boolean, default=True)


class WithdrawalsModel(Base):
    __tablename__ = "cash_register_withdrawals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cash_register_id = Column(Integer, ForeignKey("cash_register.id"))
    withdrawal = Column(Float)
