from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class SiginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Register')


class ConfirmSignupForm(FlaskForm):
    code = StringField('Verification Code', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')


class ForgotPasswordConfirmationForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField(
        'New Password', validators=[DataRequired()])
    repeat_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                           EqualTo('new_password')])
    submit = SubmitField('Submit')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField(
        'New Password', validators=[DataRequired()])
    repeat_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                           EqualTo('new_password')])
    submit = SubmitField('Request Password Change')
