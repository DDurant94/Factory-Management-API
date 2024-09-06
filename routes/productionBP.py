from flask import Blueprint
from controllers.productionController import save,find_all

production_blueprint = Blueprint('production_bp',__name__)
production_blueprint.route("/add-production-product",methods=['POST'])(save)
production_blueprint.route("/all-production",methods=["GET"])(find_all)