from flask import request, jsonify
from models.schemas.productionSchema import production_schema,all_production_schema
from services import productionService
from marshmallow import ValidationError
from caching import cache

def save():
  try:
    production_data = production_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    production_save = productionService.save(production_data)
    return production_schema.jsonify(production_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400
  
@cache.cached(timeout=60)
def find_all():
  all_production = productionService.find_all()
  return all_production_schema.jsonify(all_production)

