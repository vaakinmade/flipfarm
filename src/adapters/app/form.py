from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired


class RegisterForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email(), Length(min=5)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8),
                                                     EqualTo('confirm', message='Passwords mismatch')])
    confirm = PasswordField("Repeat Password")
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email(), Length(min=5)])
    password = PasswordField("Password", validators=[InputRequired()])


class ResetPasswordRequestForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    # submit = SubmitField('Reset password')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # submit = SubmitField('Request Password Reset')
