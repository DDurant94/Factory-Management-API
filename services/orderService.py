from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db

from models.order import Order
from models.customer import Customer
from models.product import Product
from models.orderProduct import order_product

def save(order_data):
  with Session(db.engine) as session:
    with session.begin():
      product_ids = [product['product_id'] for product in order_data['products']]
      quantities = {product['product_id']: product['quantity'] for product in order_data['products']}
      
      products = session.execute(select(Product).where(Product.id.in_(product_ids))).scalars().all()
      
      customer_id = order_data['customer_id']
      customer = session.execute(select(Customer).where(Customer.id == customer_id)).scalars().first()
      
      if len(products) != len(product_ids):
        raise ValueError("One or more products do not exist")
      
      if not customer:
        raise ValueError(f"Customer with ID {customer_id} does not exist")
      
      new_order = Order(date=order_data['date'], customer_id=customer_id)
      session.add(new_order)
      session.flush()
      
      for product in products:
        update_product = session.execute(select(Product).where(Product.id==product.id)).scalars().first()
        update_product.id=update_product.id 
        update_product.name=update_product.name
        update_product.price=update_product.price
        update_product.quantity= product.quantity - quantities[product.id]
        
        session.execute(order_product.insert().values(order_id=new_order.id, product_id=product.id, quantity=quantities[product.id]))
        
      session.commit()
      session.flush()
    session.refresh(new_order)
    
    for product in new_order.products:
      session.refresh(product)
      
    return new_order
  
def find_all():
  order_query = select(Order)
  orders = db.session.execute(order_query).scalars().all()
  return orders