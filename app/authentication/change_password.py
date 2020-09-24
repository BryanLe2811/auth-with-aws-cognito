import boto3
from flask import request, redirect, url_for, render_template, session, flash
from app.authentication.forms import ChangePasswordForm
from app.authentication import user_bp
from flask_login import login_required
from config import Config


@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.repeat_password.data

        client = boto3.client('cognito-idp', region_name=Config.REGION)
        try:
            resp = client.change_password(
                PreviousPassword=old_password,
                ProposedPassword=new_password,
                AccessToken=session['access_token']
            )
            print(f'Sign in respone: {resp}')
            flash('Your password was changed successfully')
            return redirect(url_for('authentication.change_password'))
        except client.exceptions.UserNotFoundException as e:
            flash('User not found')
        except client.exceptions.InvalidPasswordException as e:
            flash('Password not strong enough')
        except client.exceptions.NotAuthorizedException as e:
            flash('Invalid password')
        except Exception as e:
            flash('Unable to reset your password.')
            print(e)
    return render_template('authentication/change_password.html', form=form, title='Change Password')