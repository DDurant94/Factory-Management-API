from flask import request, jsonify
from marshmallow import ValidationError
from caching import cache
from database import db

from models.schemas.orderSchema import order_schema,orders_schema
from models.product import Product
from models.orderProduct import order_product

from services import orderService


def save():
  try:
    order_data = order_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  
  try:
    order_save = orderService.save(order_data)
    return order_schema.jsonify(order_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400
  
@cache.cached(timeout=60)
def find_all():
  orders_data = orderService.find_all()
  orders = []
  for order in orders_data:
    total = 0
    order_data = {
        'order_id': order.id,
        'order_date': order.date,
        'customer': {
            'customer_id': order.customer.id,
            'name': order.customer.name,
            'email': order.customer.email,
            'phone': order.customer.phone
        },
        'products': [],
        'total': []
    }
    results = db.session.query(
        Product.id,
        Product.name,
        Product.price,
        order_product.c.quantity
    ).join(order_product, Product.id == order_product.c.product_id).filter(order_product.c.order_id == order.id).all()
    
    cart_total = 0 
    total += cart_total
    for product_id, name, price, quantity in results:
      product_data = {
          'product_id': product_id,
          'name': name,
          'price': price,
          'quantity': quantity,
          'item_total': price * quantity
      }
      
      total += product_data['item_total']
      order_data['products'].append(product_data)
    order_data['total'].append(total)
    orders.append(order_data)   
  return jsonify(orders)