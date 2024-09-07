from marshmallow import fields
from schema import ma

class OrderSchema(ma.Schema):
  id = fields.Integer(required=False)
  date = fields.Date(required=True)
  customer_id = fields.Integer(required=True)
  products = fields.List(fields.Nested(lambda:OrderProductSchema), required=True)
  
  class Meta:
    fields = ('id', 'date', 'customer_id', 'products')
  
class OrderProductSchema(ma.Schema):
  product_id = fields.Integer(required=True)
  quantity = fields.Integer(required=True)
  
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

