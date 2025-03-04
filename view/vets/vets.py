from model.check_login import check_logged_in
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from flask import render_template, session, redirect
from mysql.connector import DatabaseError
from model.model import db_config

vets_bp = Blueprint('vets_bp', __name__, template_folder='templates')

@vets_bp.route('/vets')
@check_logged_in
def vet_monitor():
    if session['role'] == 'a':
        try:
            with UseDatabase(db_config) as cursor:
                _SQL = "SELECT * FROM vets"

                cursor.execute(_SQL)

                results = cursor.fetchall()

            headers = ("ID Weterynarza", "Imię weterynarza", "Nazwisko weterynarza", "Rodzaj wizyty")
            return render_template('vets.html',
                                   headers=headers,
                                   table=results)

        except DatabaseError:
            return "Unable to connect to the database", 404
    else:
        return redirect('/')