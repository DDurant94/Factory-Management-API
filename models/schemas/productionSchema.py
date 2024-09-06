from marshmallow import fields
from schema import ma

class ProductionSchema(ma.Schema):
  id = fields.Integer(required=False)
  product_id= fields.Integer(required=True)
  quantity = fields.Integer(required=True)
  date = fields.Date(required=True)
  
  class Meta: 
    fields = ("id", "product_id", "quantity", "date")
    
production_schema = ProductionSchema()
all_production_schema = ProductionSchema(many=True)
  
  