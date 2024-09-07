from flask import request, jsonify
from marshmallow import ValidationError
from caching import cache
from database import db

from models.schemas.orderSchema import order_schema,orders_schema

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
  orders = orderService.find_all()
  all_orders = []
  total = 0
  for order in orders:
    order_details={
      "order_id": order.id,
      "date": order.date,
      'customer_info': {
        'name': order.customer.name,
        'email': order.customer.email,
        'phone': order.customer.phone
        },
      'products':[],
      'total_cost':[]
    }
    for product in order.products:
      product_details={
        'product_id': product.product_id,
        'name': product.product.name,
        'price': product.product.price,
        'quantity': product.quantity,
        'product_total_cost': round(product.quantity * product.product.price,2)
      }
      order_details['products'].append(product_details)
      total+= product.quantity * product.product.price
    order_details['total_cost'].append(round(total*0.09+total,2))
    all_orders.append(order_details)
  return jsonify(all_orders)