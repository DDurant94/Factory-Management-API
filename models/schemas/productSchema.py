from marshmallow import fields, validate
from schema import ma

class ProductSchema(ma.Schema):
  id = fields.Integer(required=False)
  name = fields.String(required=True, validate=validate.Length(min=1))
  price = fields.Float(required=True, validate=validate.Range(min=0))
  quantity = fields.Integer(required=True, validate=validate.Range(min=0))
  
  class Meta:
    fields=("id","name","price","quantity")
      
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)