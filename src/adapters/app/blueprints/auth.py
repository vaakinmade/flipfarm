import functools
import logging

from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from dependency_injector.wiring import inject, Provide
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse

from src.domain.ports import register_user_factory, update_user_factory
from src.domain.ports.user_service import UserService, UserDBOperationError
from src.adapters.db.user_repository import UserRepository
from src.main.config import get_db, PASSWORD_RESET_TOKEN_USE, ACCOUNT_ACTIVATION_TOKEN_USE, \
    PASSWORD_RESET_EMAIL_SUBJECT, ACCOUNT_ACTIVATION_EMAIL_SUBJECT

from src.main.containers import Container
from src.adapters.app.form import RegisterForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from src.adapters.app.email import Email
from src.domain.ports.user_service import verify_token


blueprint = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        load_logged_in_user()
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@blueprint.before_request
@inject
def load_logged_in_user(user_service: UserService = Provide[Container.user_package.user_service]):
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            user_service.get_user_by_id(user_id)
        )


@blueprint.route('/register', methods=('GET', 'POST'))
@inject
def register(user_service: UserService = Provide[Container.user_package.user_service]):
    form = RegisterForm()
    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm']

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not confirm_password:
            error = 'Confirm Password'
        elif not validate_password(password, confirm_password):
            error = "Passwords must match"

        if error is None and user_service.get_user_by_email(email):
            error = "An account with that email already exists"

        if not error:
            try:
                user = register_user_factory(email=email.lower(), password=password)
                created_user = user_service.create(user)
            except UserDBOperationError as err:
                error = "Sorry, we were unable to register you. Please try again later."
                logging.error(f"Something went wrong with database operation {err}")
            else:
                email = Email(token_use=ACCOUNT_ACTIVATION_TOKEN_USE, subject=ACCOUNT_ACTIVATION_EMAIL_SUBJECT,
                              user=created_user.__dict__, template_html="email/activate_account.html",
                              template_text="email/activate_account.txt")
                email.send_user_email()
                flash("We have sent a unique activation link to your email. Click on it to activate your account.",
                      "Account activation")
                return render_template('auth/activate_account.html', title="Account activation", active_link=False)

        flash(error, "Account creation error")
    return render_template('auth/register.html', form=form, title="Sign up", error=error)


def validate_password(password, confirm):
    if password != confirm:
        return False
    return True


@blueprint.route('/login', methods=('GET', 'POST'))
@inject
def login(user_service: UserService = Provide[Container.user_package.user_service]):
    if session.get('user_id') is not None:
        return redirect(url_for('home.index'))

    form = LoginForm()
    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = user_service.get_user_by_email(email=email.lower())
        if not user or not check_password_hash(user["password"], password):
            error = 'Incorrect email/password'
        elif user.get('is_active') is False:
            error = 'Click on the link sent to your email to activate your account.'

        if not error:
            session.clear()
            session['user_id'] = user["id_"]
            session['email'] = user["email"]
            session['id'] = user["id"]

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home.index')
            return redirect(next_page)
            # return redirect(url_for("home.index"))

        flash(error, 'Authentication error')
    return render_template('auth/login.html', form=form, title="Sign in", error=error)


@blueprint.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("home.index"))


@blueprint.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    if session.get('user_id') is not None:
        return redirect(url_for('home.index'))

    form = ResetPasswordRequestForm()
    if request.method == 'POST':
        email = request.form['email']
        user_service = UserService(UserRepository(get_db))
        user = user_service.get_user_by_email(email=email)
        if user:
            email = Email(token_use=PASSWORD_RESET_TOKEN_USE, subject=PASSWORD_RESET_EMAIL_SUBJECT, user=user,
                          template_html="email/reset_password.html", template_text="email/reset_password.txt")
            email.send_user_email()
        flash("Check your email for password reset instructions", "Password recovery")
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@blueprint.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if session.get('user_id') is not None:
        return redirect(url_for('home.index'))

    form = ResetPasswordForm()
    error = None

    user_id = verify_token(token=token, token_use=PASSWORD_RESET_TOKEN_USE)
    user_service = UserService(UserRepository(get_db))
    user = user_service.get_user_by_id(user_id)
    if not user:
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        if not request.form['password']:
            error = 'Password is required.'
        elif not request.form['confirm_password']:
            error = 'Confirm Password'
        elif not validate_password(request.form['password'], request.form['confirm_password']):
            error = "Passwords must match"

        if not error:
            try:
                user_ = update_user_factory(id_=user.get("id_"), password=request.form['password'])
                user_service.set_password(user_)
            except UserDBOperationError as err:
                error = "Sorry, password reset failed. Please try again later."
                logging.error(f"Something went wrong with database operation during password reset {err}")
            else:
                flash('Your password has been reset', 'Password recovery')
                return redirect(url_for("auth.login"))

        flash(error, 'Password recovery error')

    return render_template('auth/reset_password.html', form=form, error=error, token=token)


@blueprint.route("activate_account/<token>", methods=['GET'])
def activate_account(token):
    if session.get('user_id') is not None:
        return redirect(url_for('home.index'))

    error = None
    user_id = verify_token(token=token, token_use=ACCOUNT_ACTIVATION_TOKEN_USE)
    user_service = UserService(UserRepository(get_db))
    user = user_service.get_user_by_id(user_id)

    if not user:
        error = "Sorry, your activation link is no longer valid. Please request another activation link"
        flash(error, "Account activation")
    else:
        try:
            user_ = update_user_factory(id_=user.get("id_"), is_active=True)
            user_service.activate_user(user_)
        except UserDBOperationError as err:
            error = "Sorry, we were unable to activate your account. Please request another activation link"
            logging.error(f"Something went wrong with database operation during account activation {err}")
        else:
            flash("Your account has now been activated.", "Account activation")

    return render_template('auth/activate_account.html', title='Account activation', error=error, token=token,
                           active_link=True)
