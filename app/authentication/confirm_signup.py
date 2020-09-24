import boto3
from flask import redirect, url_for, render_template, session, flash
from flask_login import current_user
from app.authentication.forms import ConfirmSignupForm
from app.authentication import user_bp
from app.authentication.encrypt import get_secret_hash
from config import Config


@user_bp.route('/confirm_signup', methods=['GET', 'POST'])
def confirm_signup():
    form = ConfirmSignupForm()

    if current_user.is_authenticated:
        return redirect(url_for('authentication.index'))

    if form.validate_on_submit():
        code = form.code.data
        username = form.username.data

        client = boto3.client('cognito-idp', region_name=Config.REGION)
        try:
            resp = client.confirm_sign_up(
                ClientId=Config.APP_CLIENT_ID,
                SecretHash=get_secret_hash(username),
                Username=username,
                ConfirmationCode=code,
            )
            print(f'Confirm Sign Up respone: {resp["ResponseMetadata"]["HTTPStatusCode"]}')
            flash('You have successfully registered.')
            return redirect(url_for('authentication.signin'))
        except client.exceptions.UserNotFoundException as e:
            flash('User not found')
        except client.exceptions.CodeMismatchException as e:
            flash('Invalid code inserted')
        except client.exceptions.ExpiredCodeException as e:
            flash('Your code is expired')
        except client.exceptions.NotAuthorizedException as e:
            flash('User is disabled')
        except Exception as e:
            flash('Unable to verify your account.')
            print(e)
    return render_template('authentication/confirm_signup.html', form=form, title='Verify Sign Up')