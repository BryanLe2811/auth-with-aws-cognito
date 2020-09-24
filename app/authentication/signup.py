import boto3
from flask import redirect, url_for, render_template, session, flash
from flask_login import current_user
from botocore.config import Config as Cf
from app.authentication.forms import SignupForm
from app.authentication import user_bp
from app.authentication.encrypt import get_secret_hash
from config import Config


@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if current_user.is_authenticated:
        return redirect(url_for('authentication.index'))

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.repeat_password.data

        client = boto3.client('cognito-idp',region_name=Config.REGION)
        try:
            resp = client.sign_up(
                ClientId=Config.APP_CLIENT_ID,
                SecretHash=get_secret_hash(username),
                Username=username,
                Password=password,
                UserAttributes=[
                    {
                        'Name': "email",
                        'Value': email
                    }
                ],
                ValidationData=[
                    {
                        'Name': "email",
                        'Value': email
                    }
                ])
            print('Sign up Successfully')
            return redirect(url_for('authentication.confirm_signup'))

        except client.exceptions.UsernameExistsException as e:
            flash('This username already exists')
            return redirect(url_for('authentication.signup'))
        except client.exceptions.InvalidPasswordException as e:
            flash('Password not strong enough')
            return redirect(url_for('authentication.signup'))
        except client.exceptions.UserLambdaValidationException as e:
            flash('This email already exists')
            return redirect(url_for('authentication.signup'))
        except Exception as e:
            flash(e)
            return redirect(url_for('authentication.signup'))

    return render_template('authentication/signup.html', form=form, title='Sign Up')
