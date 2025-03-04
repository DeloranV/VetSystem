from model.check_login import check_logged_in
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from model.model import db_config
from flask import session, render_template
from mysql.connector import DatabaseError

appointments_bp = Blueprint('appointments_bp', __name__)

@appointments_bp.route('/appointments')
@check_logged_in
def appointments():
    try:
        with UseDatabase(db_config) as cursor:
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