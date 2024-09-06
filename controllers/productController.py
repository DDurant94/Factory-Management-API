from flask import request, jsonify
from models.schemas.productSchema import product_schema,products_schema
from services import productService
from marshmallow import ValidationError
from caching import cache

def save():
  try:
    product_data = product_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    product_save = productService.save(product_data)
    return product_schema.jsonify(product_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400
  
@cache.cached(timeout=60)
def find_all():
  products = productService.find_all()
  return products_schema.jsonify(products), 200
  