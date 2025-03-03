from secrets import token_urlsafe
from mysql.connector import DatabaseError
from flask import Flask, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from model.check_login import check_logged_in, check_logged_out
from model.dbContextManager import UseDatabase
from api.api import api_bp
from model.model import db_config
#(TODO) BETTER ERROR HANDLING - EVERY PROBLEM GIVING THE SAME MESSAGE - SPLIT INTO SEPERATE ERRORS AND PRINT ERROR TRACE

app = Flask(__name__)
app.secret_key = 'secret'

app.register_blueprint(api_bp)

app.config['dbconfig'] = db_config

@app.route('/')
@app.route('/login')
@check_logged_out
def home():
    return render_template('login.html',
                           the_title = "Login page")

@app.route('/register')
def register():
    return render_template('register.html',
                           the_title = "Register page")

@app.route('/createaccount', methods=['POST'])
def create_account():
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
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

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form['email']
    password = request.form['password']

    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
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

@app.route('/appointments')
@check_logged_in
def appointments():
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            if session['role'] == 'u':
                _SQL = '''SELECT app_id, pet_id, pet_name, vet_name, vet_surname, appointment_type, scheduled
                FROM appointments_view WHERE owner_id=%s'''

                cursor.execute(_SQL, (session['userid'],))

                headers = ("ID Wizyty", "ID Zwierzęcia", "Imie zwierzęcia", "Imię weterynarza", "Nazwisko weterynarza",
                           "Rodzaj wizyty", "Termin wizyty")
            else:
                _SQL = '''SELECT * FROM appointments'''

                cursor.execute(_SQL)

                headers = ("ID Wizyty", "ID Zwierzęcia", "ID Weterynarza","ID Zasobu", "Rodzaj wizyty",
                           "Termin wizyty")

            results = cursor.fetchall()

        return render_template('appointments.html',
                               table=results,
                               headers=headers)
    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/pets') #(TODO) PET INFO EDITING
@check_logged_in
def pets():
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
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


@app.route('/account')  #(TODO) VIEW/EDIT ACC INFO
@check_logged_in
def account_page():
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = '''SELECT name, surname, email, phone FROM users
            WHERE id=%s'''

            cursor.execute(_SQL, (session['userid'],))
            results = cursor.fetchall()

            return render_template('account.html',
                                   data=results)

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/stock')
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

@app.route('/vets')
@check_logged_in
def vet_monitor():
    if session['role'] == 'a':
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
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

@app.route('/users')
@check_logged_in
def users():
    if session['role'] == 'a':
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
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


@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('name')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)