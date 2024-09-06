from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List,Dict
from models.orderProduct import order_product

class Product(Base):
  __tablename__ = 'Products'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]= mapped_column(db.String(100),nullable=False)
  price: Mapped[float] = mapped_column(db.Float,nullable=False)
  quantity: Mapped[int] = mapped_column(db.Integer,nullable=False)
  
  production: Mapped[List["Production"]] = db.relationship(back_populates="product")
  orders: Mapped[List['Order']] = db.relationship(secondary=order_product,back_populates="products")