from flask import Flask
from database import db
from schema import ma
from limiter import limiter
from caching import cache

def create_app(config_name):
  app = Flask(__name__)
  
  app.config.from_object(f'config.{config_name}')
  db.init_app(app)
  ma.init_app(app)
  cache.init_app(app)
  limiter.init_app(app)
  
  return app


def blue_print_config(app):
  # app.register_blueprint(customer_blueprint, url_prefix='/customers')
  # app.register_blueprint(customer_account_blueprint,url_prefix='/customer-accounts')
  # app.register_blueprint(order_blueprint,url_prefix='/orders')
  # app.register_blueprint(product_blueprint,url_prefix='/products')
  pass

def configure_rate_limit():
  # limiter.limit("5 per day")(customer_blueprint)
  pass



if __name__ == '__main__':
  app = create_app('DevelopmentConfig')
  
  blue_print_config(app)
  configure_rate_limit()
  
  with app.app_context():
    db.create_all()
    
  app.run(debug=True)