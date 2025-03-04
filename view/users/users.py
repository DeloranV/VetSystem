from model.check_login import check_logged_in
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from flask import render_template, session, redirect
from mysql.connector import DatabaseError
from model.model import db_config

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users')
@check_logged_in
def users():
    if session['role'] == 'a':
        try:
            with UseDatabase(db_config) as cursor:
                _SQL = "SELECT id, name, surname, api_key, email, phone FROM users"

                cursor.execute(_SQL)

                results = cursor.fetchall()

            headers = ("ID użytkownika", "Imię", "Nazwisko", "Klucz API",
                       "Email", "Telefon")
            return render_template('users.html',
                                   headers=headers,
                                   table=results)

        except DatabaseError:
            return "Unable to connect to the database", 404
    else:
        return redirect('/')