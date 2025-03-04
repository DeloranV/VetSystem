from model.check_login import check_logged_in
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from flask import render_template, session, redirect
from mysql.connector import DatabaseError

stock_bp = Blueprint('stock_bp', __name__, template_folder='templates')

@stock_bp.route('/stock')
@check_logged_in    #(TODO) MODIFY DECORATOR - CHECK_USER_LOGGED_IN AND CHECK_ADMIN_LOGGED_IN
def stock_monitor():
    if session['role'] == 'a':
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
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