import boto3
from flask import redirect, url_for, render_template, flash
from flask_login import current_user
from app.authentication.forms import ForgotPasswordConfirmationForm
from app.authentication import user_bp
from app.authentication.encrypt import get_secret_hash
from config import Config


@user_bp.route('/confirm_forgot_password', methods=['GET', 'POST'])
def confirm_forgot_password():
    form = ForgotPasswordConfirmationForm()

    if current_user.is_authenticated:
        return redirect(url_for('authentication.index'))

    if form.validate_on_submit():
        code = form.code.data
        username = form.username.data
        new_password = form.repeat_password.data

        client = boto3.client('cognito-idp', region_name=Config.REGION)
        try:
            resp = client.confirm_forgot_password(
                ClientId=Config.APP_CLIENT_ID,
                SecretHash=get_secret_hash(username),
                Username=username,
                ConfirmationCode=code,
                Password=new_password
            )
            print(f'Sign in respone: {resp}')
            return redirect(url_for('authentication.signin'))
        except client.exceptions.UserNotFoundException as e:
            flash('User not found')
        except client.exceptions.CodeMismatchException as e:
            flash('Invalid code inserted')
        except client.exceptions.InvalidPasswordException as e:
            flash('Password not strong enough')
        except Exception as e:
            flash('Unable to reset your password.')
            print(e)
    return render_template('authentication/confirm_forgot_password.html', form=form, title='Reset Password')