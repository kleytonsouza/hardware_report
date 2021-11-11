from flask import render_template, redirect, url_for, flash, request
from ..models import *
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
                next = url_for('auth.equips_list')
            flash('Login efetuado, bem vindo!!', 'login')
            return redirect(next)
        flash('Usuário ou senha errado(s).', "wrong")
    if request.args.get("next"):
        flash("Faça login para responder ao questionário.", 'cad')
    return render_template('auth/login.html', form=form)


@login_required
@auth.route('/equips_list', methods=['GET', 'POST'])
def equips_list():
    equipments = Equipment.query
    return render_template('auth/equips_list.html', equipments=equipments)


@login_required
@auth.route('/users_list', methods=['GET', 'POST'])
def users_list():
    users = User.query
    return render_template('auth/users_list.html', users=users)


@login_required
@auth.route('/calls_list', methods=['GET', 'POST'])
def calls_list():
    calls = Call.query
    return render_template('auth/calls_list.html', calls=calls)


@auth.route('/api/equips')
def equips_data():

    query = Equipment.query

    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Equipment.type.like(f'%{search}%'),

        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['equip_id', 'equip_user_id', 'model', 'brand', 'type']:
            col_name = 'equip_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Equipment, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [equip.to_dict() for equip in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Equipment.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/api/users')
def users_data():

    query = User.query

    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.user_name.like(f'%{search}%'),

        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['user_id', 'user_name', 'user_team_id', 'user_subteam_id']:
            col_name = 'user_name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/api/calls')
def calls_data():

    query = Call.query

    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Call.call_open.like(f'%{search}%'),

        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['call_id', 'call_equipment_id', 'call_open', 'call_close']:
            col_name = 'call_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Call, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [call.to_dict() for call in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Call.query.count(),
        'draw': request.args.get('draw', type=int),
    }