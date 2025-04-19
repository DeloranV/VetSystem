from flask import Flask, url_for
from api.api import api_bp
from view.users.users import users_bp
from view.auth.auth import auth_bp
from view.pets.pets import pet_bp
from view.vets.vets import vets_bp
from view.stock.stock import stock_bp
from view.account.account import acc_bp
from view.appointments.appointments import appointments_bp
from model.model import _db_config
#(TODO) BETTER ERROR HANDLING - EVERY PROBLEM GIVING THE SAME MESSAGE - SPLIT INTO SEPERATE ERRORS AND PRINT ERROR TRACE

app = Flask(__name__)
app.secret_key = 'secret'

app_blueprints = (api_bp, users_bp, auth_bp, pet_bp, vets_bp, stock_bp, acc_bp, appointments_bp)

for bp in app_blueprints:
    app.register_blueprint(bp)

app.config['dbconfig'] = _db_config

if __name__ == '__main__':
    app.run(debug=True)