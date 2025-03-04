from flask import Blueprint, jsonify
from model.check_api import check_api_key
from model.dbContextManager import UseDatabase
from mysql.connector import DatabaseError
from flask import session, request, Response
from random import randrange
from model.model import db_config

api_bp = Blueprint('api_bp', __name__) #(TODO) URL PREFIX

@api_bp.route('/api/appointments')
@api_bp.route('/api/appointments/<int:app_id>')
@check_api_key
def appointments_api(app_id:int = None) -> str | tuple | tuple:
    try:
        with UseDatabase(db_config) as cursor:
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

@api_bp.route('/api/pets')
@api_bp.route('/api/pets/<int:pet_id>')
@check_api_key
def pets_api(pet_id:int = None) -> str | tuple:
    try:
        with UseDatabase(db_config) as cursor:
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

@api_bp.route('/api/user/pets')
@check_api_key
def user_pets_api() -> Response | tuple:
    try:
        with UseDatabase(db_config) as cursor:

            _SQL = '''SELECT id, name FROM pets WHERE owner_id=%s'''

            cursor.execute(_SQL, (session['userid'],))
            results = cursor.fetchall()

            return jsonify(results)

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/resources')
@check_api_key
def resources_api() -> str | tuple:
    try:
        with UseDatabase(db_config) as cursor:
            _SQL = '''SELECT * FROM resources'''

            cursor.execute(_SQL)
            results = cursor.fetchall()

            return results

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/vets')
@api_bp.route('/api/vets/<int:vet_id>')
@check_api_key
def vets_api(vet_id:int = None) -> str | tuple:
    try:
        with UseDatabase(db_config) as cursor:
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

@api_bp.route('/api/appointments', methods=['POST'])
@check_api_key
def add_app_api() -> str | tuple:
    try:
        app_data = request.get_json()
        # change to unique api key identification
        with UseDatabase(db_config) as cursor:
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

            if app_data['appointment_type'] == 'd':
                resource_used = 1
            elif app_data['appointment_type'] == 'k':
                resource_used = 3
            elif app_data['appointment_type'] == 'z':
                resource_used = 4

            _SQL = '''INSERT INTO appointments(pet_id, vet_id, resource_id, appointment_type, scheduled) 
                    VALUES(%s, %s, %s, %s, %s)'''

            cursor.execute(_SQL, (app_data['pet_id'],
                                  random_vet_id,
                                  resource_used,
                                  app_data['appointment_type'],
                                  app_data['scheduled']))

            _SQL = '''UPDATE resources SET amount = amount - %s WHERE id=%s'''

            amount_used = randrange(1, 10)

            cursor.execute(_SQL, (amount_used,
                                  resource_used))

        return "Successfully added new appointment", 201

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/pets', methods=['POST'])
@check_api_key
def add_pet_api() -> str | tuple:
    try:
        pet_data = request.get_json()
          #change to unique api key identification
        with UseDatabase(db_config) as cursor:
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

@api_bp.route('/api/vets', methods=['POST'])
@check_api_key
def add_vet_api() -> str | tuple:
    try:
        vet_data = request.get_json()
        # change to unique api key identification
        with UseDatabase(db_config) as cursor:
            _SQL = '''INSERT INTO vets(name, surname, appointment_type) VALUES(%s, %s, %s)'''

            cursor.execute(_SQL, (vet_data['name'],
                                  vet_data['surname'],
                                  vet_data['appointment_type']))

        return "Successfully added new vet", 201

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/account', methods=['PATCH'])
@check_api_key
def modify_account_api() -> str | tuple:
    try:
        account_data = request.get_json()

        for key, value in account_data.items():

            if key not in('name', 'surname', 'email', 'phone', 'role'):
                return "Unable to change value", 404
            if value == '':
                return "No value provided", 404

            with UseDatabase(db_config) as cursor:
                _SQL = f'''UPDATE users SET {key}=%s WHERE id=%s'''

                cursor.execute(_SQL, (value, session['userid']))

        return "Successfully updated user data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/users/<int:user_id>', methods=['PATCH'])
@check_api_key
def modify_user_api(user_id:int) -> str | tuple:
    try:
        account_data = request.get_json()

        for key, value in account_data.items():

            if key not in('name', 'surname', 'email', 'phone'):
                return "Unable to change value", 404

            if value == '':
                return "No value provided", 404

            with UseDatabase(db_config) as cursor:
                _SQL = f'''UPDATE users SET {key}=%s WHERE id=%s'''

                cursor.execute(_SQL, (value, user_id))

        return "Successfully updated user data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/appointments/<int:app_id>', methods=['PATCH'])
@check_api_key
def modify_appointment_api(app_id:int) -> str | tuple:
    try:
        appointment_data = request.get_json()
        for key, value in appointment_data.items():

            if key != 'scheduled':
                return "Can only change scheduled date"

            if value == '':
                return "No value provided", 404

            # change to unique api key identification
            with UseDatabase(db_config) as cursor:
                _SQL = f"UPDATE appointments SET {key}=%s WHERE id=%s"

                cursor.execute(_SQL, (value, app_id))

        return "Successfully updated appointment data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/pets/<int:pet_id>', methods=['PATCH'])
@check_api_key
def modify_pet_api(pet_id:int) -> str | tuple:
    try:
        pet_data = request.get_json()
        for key, value in pet_data.items():

            if key not in ('name', 'type', 'age'):
                return "Unable to change value", 404

            if value == '':
                return "No value provided", 404

            with UseDatabase(db_config) as cursor:
                _SQL = f"UPDATE pets SET {key}=%s WHERE id=%s"

                cursor.execute(_SQL, (value, pet_id))

        return "Successfully updated pet data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/resources/<int:res_id>', methods=['PATCH'])
@check_api_key
def modify_resource_api(res_id:int) -> str | tuple:
    try:
        res_data = request.get_json()
        for key, value in res_data.items():

            if key not in ('name', 'amount'):
                return "Unable to change value", 404

            if value == '':
                return "No value provided", 404

            with UseDatabase(db_config) as cursor:
                _SQL = f"UPDATE resources SET {key}=%s WHERE id=%s"

                cursor.execute(_SQL, (value, res_id))

        return "Successfully updated resource data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/vets/<int:vet_id>', methods=['PATCH'])
@check_api_key
def modify_vet_api(vet_id:int) -> str | tuple:
    try:
        vet_data = request.get_json()
        for key, value in vet_data.items():

            if key not in ('name', 'surname', 'appointment_type'):
                return "Unable to change value", 404

            if value == '':
                return "No value provided", 404

            with UseDatabase(db_config) as cursor:
                _SQL = f"UPDATE vets SET {key}=%s WHERE id=%s"

                cursor.execute(_SQL, (value, vet_id))

        return "Successfully updated vet data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/resupply/<int:res_id>', methods=['PATCH'])
@check_api_key
def modify_stock_api(res_id:int) -> str | tuple:
    try:
        res_data = request.get_json()
        with UseDatabase(db_config) as cursor:
            _SQL = '''UPDATE resources SET amount=amount+%s WHERE id=%s'''

            cursor.execute(_SQL, (res_data['amount'], res_id))

            return "Resupplied resource successfully"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/appointments/<int:app_id>', methods=['DELETE'])
@check_api_key
def delete_app_api(app_id:int) -> str | tuple:
    try:
        with UseDatabase(db_config) as cursor:
            _SQL = '''DELETE FROM appointments WHERE id=%s'''

            cursor.execute(_SQL, (app_id,))

        return "Successfully removed appointment data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/pets/<int:pet_id>', methods=['DELETE'])
@check_api_key
def delete_pet_api(pet_id:int) -> str | tuple:
    try:
        with UseDatabase(db_config) as cursor:
            _SQL = '''DELETE FROM pets WHERE id=%s'''

            cursor.execute(_SQL, (pet_id,))

        return "Successfully removed pet data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/vets/<int:vet_id>', methods=['DELETE'])
@check_api_key
def delete_vet_api(vet_id:int) -> str | tuple:
    try:
        with UseDatabase(db_config) as cursor:
            _SQL = '''DELETE FROM vets WHERE id=%s'''

            cursor.execute(_SQL, (vet_id,))

        return "Successfully removed vet data"

    except DatabaseError:
        return "Unable to connect to the database", 404

@api_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@check_api_key
def delete_user_api(user_id:int) -> str | tuple:
    try:
        with UseDatabase(db_config) as cursor:
            _SQL = '''DELETE FROM users WHERE id=%s'''

            cursor.execute(_SQL, (user_id,))

        return "Successfully removed user data"

    except DatabaseError:
        return "Unable to connect to the database", 404
