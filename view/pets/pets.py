from model.check_login import check_logged_in
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from model.model import db_config
from flask import render_template, session
from mysql.connector import DatabaseError

pet_bp = Blueprint('pet_bp', __name__, template_folder='templates')

@pet_bp.route('/pets')
@check_logged_in
def pets() -> str | tuple:
    try:
        with UseDatabase(db_config) as cursor:
            if session['role'] == 'u':
                _SQL = '''SELECT id, name, type, age FROM pets_view 
                WHERE owner_id=%s'''

                cursor.execute(_SQL, (session['userid'],))

                headers = ("ID Zwierzęcia", "Imię zwierzęcia", "Gatunek zwierzęcia", "Wiek")
            else:
                _SQL = '''SELECT * FROM pets'''

                cursor.execute(_SQL)

                headers = ("ID Zwierzęcia", "ID Właściciela", "Imię zwierzęcia", "Gatunek zwierzęcia", "Wiek")

            results = cursor.fetchall()

        return render_template('pets.html',
                               headers=headers,
                               table=results)

    except DatabaseError:
        return "Unable to connect to the database", 404