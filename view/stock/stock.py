from model.check_login import check_logged_in
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from flask import render_template, session, redirect, Response
from mysql.connector import DatabaseError
from model.model import db_config

stock_bp = Blueprint('stock_bp', __name__, template_folder='templates')

@stock_bp.route('/stock')
@check_logged_in
def stock_monitor() -> tuple | Response | str:
    if session['role'] == 'a':
        try:
            with UseDatabase(db_config) as cursor:
                _SQL = "SELECT * FROM resources"

                cursor.execute(_SQL)

                results = cursor.fetchall()

            headers = ("ID Zasobu", "Nazwa zasobu", "Pozostała ilość")
            return render_template('stock.html',
                                   headers=headers,
                                   table=results)

        except DatabaseError:
            return "Unable to connect to the database", 404
    else:
        return redirect('/')