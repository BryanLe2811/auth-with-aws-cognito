from flask import redirect, url_for, render_template, session, flash
from app.models import User
from flask_login import login_user, current_user, logout_user
from app import db
from app.authentication.forms import SiginForm
from app.authentication import user_bp
from app.authentication.decode_verify_jwt import lambda_handler
from app.authentication.aws_srp import AWSSRP
from config import Config


@user_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SiginForm()

    if current_user.is_authenticated:
        return redirect(url_for('authentication.index'))

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data

        try:
            aws = AWSSRP(username=username, password=password, pool_id=Config.USERPOOL_ID,
                         client_id=Config.APP_CLIENT_ID, pool_region=Config.REGION)
            resp = aws.authenticate_user()

            event =  {'message': "success",
                    "error": False,
                    "success": True,
                    "data": {
                        "id_token": resp["AuthenticationResult"]["IdToken"],
                        "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                        "access_token": resp["AuthenticationResult"]["AccessToken"],
                        "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                        "token_type": resp["AuthenticationResult"]["TokenType"]
                    }}

            token_object = event["data"]
            claims = lambda_handler(token_object, None)

            if not claims:
                flash("Unable to login")

            user = claims['cognito:username']
            email = claims['email']

            user_query = User.query.filter_by(username=username).first()
            if user_query:
                login_user(user_query, remember=remember)
            else:
                user_query = User(username=user, useremail=email)
                db.session.add(user_query)
                db.session.commit()
                login_user(user_query, remember=False)
            session['user_role'] = user_query.role
            session['access_token'] = event['data']['access_token']

            return redirect(url_for('authentication.index'))

        except Exception as e:
            flash('Unable to Sign In.')
            print(e)

    return render_template('authentication/signin.html', form=form, title='Sign In')


@user_bp.route('/signout')
def signout():
    session.clear()
    logout_user()
    return redirect(url_for('authentication.index'))
