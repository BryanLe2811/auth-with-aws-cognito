from flask import render_template
from app import db
from app.errors import errors_bp


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@errors_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@errors_bp.app_errorhandler(401)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/401.html'), 401