from model.check_login import check_logged_in
from flask.blueprints import Blueprint
from model.dbContextManager import UseDatabase
from model.model import _db_config
from flask import session, render_template
from mysql.connector import DatabaseError

acc_bp = Blueprint('acc_bp', __name__, template_folder='templates')

@acc_bp.route('/account')
@check_logged_in
def account_page() -> str | tuple:
    try:
        with UseDatabase(_db_config) as cursor:
            _SQL = '''SELECT name, surname, email, phone FROM users
            WHERE id=%s'''

            cursor.execute(_SQL, (session['userid'],))
            results = cursor.fetchall()

            return render_template('account.html',
                                   data=results)

    except DatabaseError:
        return "Unable to connect to the database", 404