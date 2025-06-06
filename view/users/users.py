from model.check_login import check_logged_in
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from flask import render_template, session, redirect, Response, url_for
from mysql.connector import DatabaseError
from model.model import _db_config

users_bp = Blueprint('users_bp', __name__, template_folder='templates')

@users_bp.route('/users')
@check_logged_in
def users() -> tuple | Response | str:
    if session['role'] == 'a':
        try:
            with UseDatabase(_db_config) as cursor:
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
        return redirect(url_for('home'))