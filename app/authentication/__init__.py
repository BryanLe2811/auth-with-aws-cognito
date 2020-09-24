from flask import Blueprint

user_bp = Blueprint('authentication', __name__)

from app.authentication import index, signin, signup, confirm_signup, forgot_password, confirm_forgot_password, change_password
