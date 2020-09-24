import boto3
from flask import redirect, url_for, render_template, flash
from flask_login import current_user
from app.authentication.forms import ForgotPasswordForm
from app.authentication import user_bp
from app.authentication.encrypt import get_secret_hash
from config import Config


@user_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if current_user.is_authenticated:
        return redirect(url_for('authentication.index'))

    if form.validate_on_submit():
        username = form.username.data

        client = boto3.client('cognito-idp', region_name=Config.REGION)
        try:
            resp = client.forgot_password(
                ClientId=Config.APP_CLIENT_ID,
                SecretHash=get_secret_hash(username),
                Username=username
            )
            return redirect(url_for('authentication.confirm_forgot_password'))
        except client.exceptions.UserNotFoundException as e:
            flash('User not found')
        except Exception as e:
            flash('Unable to reset your password.')
            print(e)
    return render_template('authentication/forgot_password.html', form=form, title='Reset Password')