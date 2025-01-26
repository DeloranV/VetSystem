from secrets import token_urlsafe
from mysql.connector import DatabaseError
from flask import Flask, render_template, request, session, request_started
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from check_api import check_api_key
from check_login import check_logged_in, check_logged_out
from dbContextManager import UseDatabase
from random import randrange

app = Flask(__name__)
app.secret_key = 'secret'

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vetAdmin',
                          'password': 'admin',
                          'database': 'vet'}

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
            return("Invalid username")
        elif not check_password_hash(passwordDB[0][0], password):
            return("Invalid password")

        session['logged_in'] = True

        return redirect('/dashboard')

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/dashboard')
@check_logged_in
def dashboard():
    return render_template('dashboard.html',
                           the_title='dashboard',
                           name=session['name'])

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
    return render_template('account.html')

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

@app.route('/api/appointments')
@app.route('/api/appointments/<int:app_id>')
@check_api_key(app)
def appointments_api(app_id=None):
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            if not app_id:
                    _SQL = '''SELECT * FROM appointments'''

                    cursor.execute(_SQL)
                    results = cursor.fetchall()

            else:
                    _SQL = '''SELECT * FROM appointments WHERE id = %s'''

                    cursor.execute(_SQL, (app_id,))
                    results = cursor.fetchall()

            return results

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/pets')
@app.route('/api/pets/<int:pet_id>')
@check_api_key(app)
def pets_api(pet_id=None):
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
                if not pet_id:
                    _SQL = '''SELECT * FROM pets'''

                    cursor.execute(_SQL)
                    results = cursor.fetchall()

                else:
                    _SQL = '''SELECT * FROM pets WHERE id = %s'''

                    cursor.execute(_SQL, (pet_id,))
                    results = cursor.fetchall()

                return results

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/resources')
@check_api_key(app)
def resources_api():
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = '''SELECT * FROM resources'''

            cursor.execute(_SQL)
            results = cursor.fetchall()

            return results

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/vets')
@app.route('/api/vets/<int:vet_id>')
@check_api_key(app)
def vets_api(vet_id=None):
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            if not vet_id:
                _SQL = '''SELECT * FROM vets'''

                cursor.execute(_SQL)
                results = cursor.fetchall()

            else:
                _SQL = '''SELECT * FROM vets WHERE id = %s'''

                cursor.execute(_SQL, (vet_id,))
                results = cursor.fetchall()

            return results

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/appointments', methods=['POST'])
@check_api_key(app)
def add_app_api():
    try:
        app_data = request.get_json()
        # change to unique api key identification
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = '''SELECT id FROM vets
                    WHERE appointment_type=%s AND id NOT IN(
                        SELECT vet_id FROM appointments
                        WHERE scheduled IN(%s))'''

            cursor.execute(_SQL, (app_data['appointment_type'],
                                  app_data['scheduled']))

            results = cursor.fetchall()
            available_vets = []

            for result in results:
                available_vets.append(result[0])

            if len(available_vets) == 0:
                return "Not available at this date"

            random_vet_id = available_vets[randrange(0, len(available_vets))]

            if app_data['appointment_type'] == 'w':
                resource_used = 3
            elif app_data['appointment_type'] == 'k':
                resource_used = 1
            elif app_data['appointment_type'] == 'z':
                resource_used = 4

            _SQL = '''INSERT INTO appointments(pet_id, vet_id, resource_id, appointment_type, scheduled) 
                    VALUES(%s, %s, %s, %s, %s)'''

            cursor.execute(_SQL, (app_data['pet_id'],
                                  random_vet_id,
                                  resource_used,
                                  app_data['appointment_type'],
                                  app_data['scheduled']))

            _SQL = '''UPDATE resources SET amount = amount - 1 WHERE id=%s'''

            cursor.execute(_SQL, (resource_used,))

        return "Successfully added new appointment", 201

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/pets', methods=['POST'])
@check_api_key(app)
def add_pet_api():
    try:
        pet_data = request.get_json()
          #change to unique api key identification
        with UseDatabase(app.config['dbconfig']) as cursor:
            if 'owner_id' in pet_data:
                _SQL = '''INSERT INTO pets(owner_id, name, type, age) VALUES(%s, %s, %s, %s)'''

                cursor.execute(_SQL, (pet_data['owner_id'],
                                      pet_data['name'],
                                      pet_data['type'],
                                      pet_data['age']))
            else:
                _SQL = '''INSERT INTO pets(owner_id, name, type, age) VALUES(%s, %s, %s, %s)'''

                cursor.execute(_SQL, (session['userid'],
                                      pet_data['name'],
                                      pet_data['type'],
                                      pet_data['age']))

        return "Successfully added new pet", 201

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/vets', methods=['POST'])
@check_api_key(app)
def add_vet_api():
    try:
        vet_data = request.get_json()
        # change to unique api key identification
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = '''INSERT INTO vets(name, surname, appointment_type) VALUES(%s, %s, %s)'''

            cursor.execute(_SQL, (vet_data['name'],
                                  vet_data['surname'],
                                  vet_data['appointment_type']))

        return "Successfully added new vet", 201

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/appointments/<int:app_id>', methods=['PATCH'])
@check_api_key(app)
def modify_appointment_api(app_id):
    try:
        appointment_data = request.get_json()
        for key, value in appointment_data.items():

            if key != 'scheduled':
                return "Can only change scheduled date"

            # change to unique api key identification
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = f"UPDATE appointments SET {key}=%s WHERE id=%s"

                cursor.execute(_SQL, (value, app_id))

        return "Successfully updated appointment data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/pets/<int:pet_id>', methods=['PATCH']) #(TODO)
@check_api_key(app)
def modify_pet_api(pet_id):
    try:
        pet_data = request.get_json()
        for key, value in pet_data.items():

            if key not in ('name', 'type', 'age'):
                return "Unable to change value", 404

            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = f"UPDATE pets SET {key}=%s WHERE id=%s"

                cursor.execute(_SQL, (value, pet_id))

        return "Successfully updated pet data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/resources/<int:res_id>', methods=['PATCH']) #(TODO)
@check_api_key(app)
def modify_resource_api(res_id):
    try:
        res_data = request.get_json()
        for key, value in res_data.items():

            if key not in ('name', 'amount'):
                return "Unable to change value", 404

            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = f"UPDATE resources SET {key}=%s WHERE id=%s"

                cursor.execute(_SQL, (value, res_id))

        return "Successfully updated resource data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/vets/<int:vet_id>', methods=['PATCH']) #(      TODO)
@check_api_key(app)
def modify_vet_api(vet_id):
    try:
        vet_data = request.get_json()
        for key, value in vet_data.items():

            if key not in ('name', 'surname', 'appointment_type'):
                return "Unable to change value", 404

            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = f"UPDATE vets SET {key}=%s WHERE id=%s"

                cursor.execute(_SQL, (value, vet_id))

        return "Successfully updated vet data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/resupply/<int:res_id>', methods=['PATCH'])
@check_api_key(app)
def modify_stock_api(res_id):
    try:
        res_data = request.get_json()
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = '''UPDATE resources SET amount=amount+%s WHERE id=%s'''

            cursor.execute(_SQL, (res_data['amount'], res_id))

            return "Resupplied resource successfully"

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/pets/<int:pet_id>', methods=['DELETE']) #(TODO)
@check_api_key(app)
def delete_pet_api(pet_id):
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = '''DELETE FROM pets WHERE id=%s'''

            cursor.execute(_SQL, (pet_id,))

        return "Successfully removed pet data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/vets/<int:vet_id>', methods=['DELETE']) #(TODO)
@check_api_key(app)
def delete_vet_api(vet_id):
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = '''DELETE FROM vets WHERE id=%s'''

            cursor.execute(_SQL, (vet_id,))

        return "Successfully removed vet data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/api/users/<int:user_id>', methods=['DELETE']) #(TODO)
@check_api_key(app)
def delete_user_api(user_id):
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = '''DELETE FROM users WHERE id=%s'''

            cursor.execute(_SQL, (user_id,))

        return "Successfully removed user data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('name')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)