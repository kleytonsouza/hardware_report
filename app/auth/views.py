from flask import render_template, redirect, url_for, flash, request
from ..models import Admin
from . import auth
from flask_login import login_user, logout_user, login_required, current_user
from ..auth.forms import LoginForm


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado do Sistema!', 'off')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_name=form.user.data).first()
        passwordb = form.password.data
        if admin is not None and admin.verify_password(passwordb):
            login_user(admin)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('auth.list')
            flash('Login efetuado, bem vindo!!', 'login')
            return redirect(next)
        flash('Usuário ou senha errado(s).', "wrong")
    if request.args.get("next"):
        flash("Faça login para responder ao questionário.", 'cad')
    return render_template('auth/login.html', form=form)


@login_required
@auth.route('/list', methods=['GET', 'POST'])
def list():
    return "<h1>To aqui</h1>"
