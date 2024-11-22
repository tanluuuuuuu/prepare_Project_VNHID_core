from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)
from sqlalchemy import BIGINT, VARCHAR, func, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime
from typing import Optional, Annotated, List
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, nullable=True, onupdate=func.now()
    )


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


int_pk = Annotated[int, mapped_column(BIGINT, primary_key=True)]
user_fk = Annotated[
    int, mapped_column(BIGINT, ForeignKey("users.telegram_id", ondelete="SET NULL"))
]
str_255 = Annotated[str, mapped_column(VARCHAR(255))]


class User(Base, TimestampMixin, TableNameMixin):
    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    full_name: Mapped[str_255]
    username: Mapped[Optional[str_255]]
    language_code: Mapped[str] = mapped_column(VARCHAR(10))
    referrer_id: Mapped[Optional[user_fk]]

    # Relationships
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")

class Product(Base, TimestampMixin, TableNameMixin):
    product_id: Mapped[int_pk]
    title: Mapped[str_255]
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(3000))
    price: Mapped[float] = mapped_column(DECIMAL(precision=16, scale=4))
    
    # Relationships
    order_products: Mapped[List["OrderProduct"]] = relationship("OrderProduct", back_populates="product")

class Order(Base, TimestampMixin, TableNameMixin):
    order_id: Mapped[int_pk]
    user_id: Mapped[user_fk]
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    products: Mapped[List["OrderProduct"]] = relationship("OrderProduct", back_populates="order")


class OrderProduct(Base, TableNameMixin):
    order_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("orders.order_id", ondelete="CASCADE"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("products.product_id", ondelete="RESTRICT"), primary_key=True
    )
    quantity: Mapped[int]

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="products")
    product: Mapped["Product"] = relationship("Product", back_populates="order_products")


# Define URL
url = URL.create(
    drivername="postgresql+psycopg2",
    username="testuser",
    password="testpassword",
    host="localhost",
    port=5432,
    database="testuser",
).render_as_string(hide_password=False)

engine = create_engine(url)  # logging
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

