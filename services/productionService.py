from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select

from models.production import Production
from models.product import Product

from services.productService import save

def save(production_data):
  with Session(db.engine) as session:
    with session.begin():
      product_id = production_data['product_id']
      product = session.execute(select(Product).where(Product.id==product_id)).scalars().first()
      product.id=product.id 
      product.name=product.name
      product.price=product.price
      product.quantity= product.quantity + production_data["quantity"]
      
      new_production = Production(product_id = production_data["product_id"], quantity = production_data["quantity"], date=production_data["date"])
      session.add(new_production)
      session.commit()
      
    session.refresh(new_production)
    
    return new_production
  
def find_all():
  query = select(Production)
  all_production = db.session.execute(query).scalars().all()
  return all_production