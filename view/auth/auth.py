from secrets import token_urlsafe
from model.check_login import check_logged_out
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from model.model import db_config
from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import DatabaseError

auth_bp = Blueprint('app_bp', __name__, template_folder='templates')

@auth_bp.route('/')
@auth_bp.route('/login')
@check_logged_out
def home():
    return render_template('login.html',
                           the_title = "Login page")

@auth_bp.route('/register')
def register():
    return render_template('register.html',
                           the_title = "Register page")

@auth_bp.route('/createaccount', methods=['POST'])
def create_account():
    try:
        with UseDatabase(db_config) as cursor:
            _SQL = '''INSERT INTO users(name, surname, password, api_key, email, phone, role)
            VALUES(%s, %s, %s, %s, %s, %s, %s)'''

            cursor.execute(_SQL, (request.form['name'],
                                  request.form['surname'],
                                  generate_password_hash(request.form['password']),
                                  token_urlsafe(10),
                                  request.form['email'],
                                  request.form['phone'],
                                  "u"))

        return redirect('/')

    except DatabaseError:
        return "Unable to connect to the database", 404

@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']

    try:
        with UseDatabase(db_config) as cursor:
            _SQL = '''SELECT id, email, name, role FROM users WHERE email = %s'''
            cursor.execute(_SQL, [email])

            results = cursor.fetchall()
            session['userid'] = results[0][0]
            session['email'] = results[0][1]
            session['name'] = results[0][2]
            session['role'] = results[0][3]

            _SQL = '''SELECT password FROM users WHERE email = %s'''
            cursor.execute(_SQL, [email])

            passwordDB = cursor.fetchall()

        if len(session['email']) == 0:
            return "Invalid username"
        elif not check_password_hash(passwordDB[0][0], password):
            return"Invalid password"

        session['logged_in'] = True

        return redirect('/appointments')

    except DatabaseError:
        return "Unable to connect to the database", 404

@auth_bp.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('name')
    return redirect('/')