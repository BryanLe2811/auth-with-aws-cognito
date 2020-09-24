from flask import render_template
from app.authentication import user_bp


@user_bp.route("/")
def index():
    return render_template('index.html');