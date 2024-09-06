from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select
from models.product import Product


def save(product_data):
  with Session(db.engine) as session:
    with session.begin():
      new_product = Product(name=product_data["name"],price=product_data["price"],quantity=product_data["quantity"])
      session.add(new_product)
      session.commit()
    session.refresh(new_product)
    return new_product
  
def find_all():
  query = select(Product)
  products = db.session.execute(query).scalars().all()
  return products