from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models.userModel import UserModel
from app import db 
from app.models.productModel import Cart
from app.forms import regLoginForm
from flask_bcrypt import Bcrypt
from datetime import datetime
from utils.cartUtils import cart_init

auth_bp = Blueprint('auth', __name__)

bcrypt = Bcrypt()

@auth_bp.route("/", methods=['POST', 'GET'])
@auth_bp.route("/<error>", methods=['POST', 'GET'])
def main_view(error=""):
    login_form = regLoginForm.LoginForm()
    register_form = regLoginForm.RegisterForm()

    def validate_username(self, username):
        if UserModel.query.filter_by(username=username.data).first():
            raise ValidationError("This username already exists. Please choose something unique")

    register_form.validate_username = validate_username

    if request.method == 'POST':
        if request.form.get('loginAction') == 'Login':
            return render_template("mainView.html", form=login_form)
        else:
            return render_template("mainView.html", form=register_form)
    return render_template("mainView.html", form=login_form, error=error)

@auth_bp.route("/login.html", methods=['GET', 'POST'])
def login():
    login_form = regLoginForm.LoginForm()
    if login_form.validate_on_submit():
        user = UserModel.query.filter_by(username=login_form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            cart_init(db, current_user)
            return redirect(url_for('dashboard.dashboard'))
    error = "Invalid Username or Password"
    return redirect(url_for('auth.main_view', error=error))

@auth_bp.route("/register.html", methods=['GET', 'POST'])
def register():
    registerForm = regLoginForm.RegisterForm()
    if registerForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            registerForm.password.data)
        checkUsername = UserModel.query.filter_by(
            username=registerForm.username.data).first()
        if (checkUsername):
            return redirect(url_for('auth.main_view', error="Username already taken"))
        new_user = UserModel(username=registerForm.username.data,
                             password=hashed_password, firstOrder=True)
        print('Creating a new cart.')
        db.session.add(new_user)
        db.session.commit()
        new_cart = Cart(userId=new_user.uuid, totalValue=0, products={})
        db.session.add(new_cart)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard.dashboard')) 

@auth_bp.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.main_view'))
