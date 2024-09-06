from flask import Blueprint
from controllers.employeeController import save, find_all

employee_blueprint = Blueprint('employee_bp',__name__)
employee_blueprint.route('/add-employee',methods=['POST'])(save)
employee_blueprint.route('/',methods=['GET'])(find_all)