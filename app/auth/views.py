from _datetime import datetime

from flask import render_template, redirect, url_for, flash, request, make_response
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from . import auth
from ..auth.forms import LoginForm, form_add_equip, form_add_user, form_edit_equip, form_edit_user, form_open_history
from ..models import *


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado do Sistema!', 'off')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.equips_list'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(id=form.user.data).first()
        passwordb = form.password.data
        if user is not None and user.verify_password(passwordb):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('auth.equips_list')
            flash('Login efetuado, bem vindo!!', 'login')
            return redirect(next)
        flash('Usuário ou senha errado(s).', "wrong")
    if request.args.get("next"):
        flash("Faça login para acessar os dados.", 'cad')
    return render_template('auth/login.html', form=form)


@login_required
@auth.route('/equips_list', methods=['GET', 'POST'])
def equips_list():
    equipments = Equipment.query
    return render_template('auth/list_equips.html', equipments=equipments)


@login_required
@auth.route('/users_list', methods=['GET', 'POST'])
def users_list():
    # users = User.query
    return render_template('auth/list_users.html')  # , users=users)


@login_required
@auth.route('/list_history', methods=['GET', 'POST'])
def list_history():
    # history = EquipmentUsageHistory.query
    return render_template('auth/list_history.html') #, history=history)


@auth.route('/api/equips')
def equips_data():
    query = Equipment.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(Equipment).join(User).filter(db.or_(
            Equipment.id.like(f'%{search}%'),
            Equipment.type.like(f'%{search}%'),
            Equipment.registry.like(f'%{search}%'),
            Equipment.model.like(f'%{search}%'),
            User.name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['id', 'type', 'model', 'registry', 'user_id']:
            col_name = 'id'
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
        'data': [equip.equip_to_dict() for equip in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Equipment.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/api/users')
def users_data():
    query = User.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(User).join(Team).filter(db.or_(
            User.name.like(f'%{search}%'),
            User.register.like(f'%{search}%'),
            Team.name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['id', 'register', 'name', 'team_id']:
            col_name = 'name'
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


@auth.route('/api/list_equipment_usage_history')
def list_equipment_usage_history():
    query = EquipmentUsageHistory.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(EquipmentUsageHistory).join(User).filter(db.or_(
            EquipmentUsageHistory.equip_id.like(f'%{search}%'),
            EquipmentUsageHistory.date_receive.like(f'%{search}%'),
            EquipmentUsageHistory.date_return.like(f'%{search}%'),
            User.name.like(f'%{search}%'),

        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['id', 'date_receive', 'date_return', 'user_id']:
            col_name = 'id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(EquipmentUsageHistory, col_name)
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
        'data': [history.to_dict() for history in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': EquipmentUsageHistory.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/add_equip', methods=['POST', 'GET'])
def add_equip():
    # classes_equips_list = Equipment.__subclasses__()
    # classes_equips_list.append(Equipment)
    #
    # for name_classe in classes_equips_list:
    #     if name_classe.__name__ == type:
    #         # form.fields.choices = name_classe.__table__.columns.keys()
    #         return render_template("auth/add_equip.html", form=form)

    form_class = form_add_equip()
    form = form_class()

    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(id=request.form.getlist("equip_user")[0]).first()
        # if request.form.get("devid") == "":
        novo_equip = Equipment(
            user_id=user.id,
            brand=request.form.get("brand"),
            model=request.form.get("model"),
            devid=request.form.get("devid"),
            add_for=user.id,
            registry=datetime.today().strftime('%d/%m/%Y'),
            general_description=request.form.get("general_description"),
            type=request.form.get('type')
        )
        db.session.add(novo_equip)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)
        return render_template("auth/add_success.html", title="Equipamento Genérico")
    return render_template("auth/add_equip.html", form=form)


@auth.route('/user_add', methods=['POST', 'GET'])
def user_add():
    form = form_add_user()

    if form.validate_on_submit() and request.method == 'POST':
        team = request.form.get("team_id")
        name = request.form.get("name")
        novo_user = User(
            name=name,
            team_id=team  # lst_teams é uma 'string' e não uma lista

        )
        db.session.add(novo_user)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error, element="Usuário " + novo_user.name)

        return render_template("auth/add_success.html", title="Novo Usuário")

    return render_template("auth/add_user.html", form=form)


@auth.route('/delete_user/', methods=['POST', 'GET'])
def delete_user():
    print(1)
    if request.method == 'POST':

        user_id = request.get_json()["user_id"]

        user = User.query.filter_by(user_id=user_id).first()

        if Equipment.query.filter_by(equip_user_id=user_id).first():
            print(3)
            print("mememe")
            return make_response('Hello, World', 201)

        db.session.delete(user)
        # try:
        db.session.commit()
        # except:
        #    db.session.rollback()
        # error = str(.__dict__['orig'])
        return render_template("auth/add_error.html")

    print("xx")
    return users_data()


@auth.route('/del_success')
def del_success():
    return render_template("auth/del_success.html")


@auth.route('/add_history', methods=['POST', 'GET'])
def add_history():
    form = form_open_history()
    error = None

    print(form.validate_on_submit())
    print(form.errors)
    print(form.data)
    if request.method == "POST":
        new_history = EquipmentUsageHistory(id=request.form.get("call_equipment"),
                                            user_id=User.query.filter_by(name=request.form.get("user_id")).first().id,
                                            equip_id=Equipment.query.filter_by(
                                                id=request.form.get("equip_id")).first().id,
                                            date_receive=request.form.get("date_receive"),
                                            observation=request.form.get("observation"),
                                            date_return=request.form.get("date_return"),
                                            )
        db.session.add(new_history)
        try:
            db.session.commit()
            flash('Histórico criado com sucesso!', 'success')
            return render_template("auth/add_success.html", title="Histórico")
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error, element="Histórico em " + new_history.id)
    elif request.method == "POST":
        error = "problema ao criar histórico!!"

    return render_template("auth/add_history.html", form=form, error=error)


@auth.route('user_edit/<id_user>', methods=['POST', 'GET'])
def user_edit(id_user):
    user_to_edit = User.query.filter_by(user_id=id_user).first()

    form_class = form_edit_user(user_to_edit)
    form = form_class()

    if form.validate_on_submit() and request.method == 'POST' and current_user.is_admin():
        try:
            # user_to_edit.user_register = request.form.getlist("user_register"),
            user_to_edit.user_name = request.form.get("user_name"),
            user_to_edit.user_team_id = request.form.get("user_team_id"),
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)
        return render_template("auth/edit_success.html", title="Usuário Editado")
    return render_template("auth/user_edit.html", form=form, user_to_edit=user_to_edit.user_id)


@auth.route('/edit_item/<id_equip>', methods=['POST', 'GET'])
def edit_item(id_equip):
    equip_to_edit = Equipment.query.filter_by(id=id_equip).first()

    if equip_to_edit.type == 'equipments':
        form_class = form_edit_equip(equip_to_edit)
        form = form_class()
        if form.validate_on_submit() and request.method == 'POST' and current_user.is_admin():
            try:
                equip_to_edit.user_id = request.form.getlist("equip_user"),
                equip_to_edit.type = request.form.get("type"),
                equip_to_edit.brand = request.form.get("brand"),
                equip_to_edit.model = request.form.get("model"),
                equip_to_edit.position = request.form.get("position"),
                equip_to_edit.general_description = request.form.get("general_description"),
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                error = str(e.__dict__['orig'])
                return render_template("auth/add_error.html", error=error)
            return render_template("auth/edit_success.html", title="Equipamento Editado")
        return render_template("auth/edit_equip.html", form=form, equip_to_edit=equip_to_edit.equip_id)
    else:
        return "Error line 1053 views"


@auth.route('/detail_item/<id_equip>', methods=['POST', 'GET'])
def detail_item(id_equip):
    equip_detail = Equipment.query.filter_by(id=id_equip).first()

    return render_template("auth/detail_equip.html", equip_detail=equip_detail)


@auth.route('/detail_user/<id_user>', methods=['POST', 'GET'])
def detail_user(id_user):
    user_detail = User.query.filter_by(id=id_user).first()

    return render_template("auth/detail_user.html", user_detail=user_detail)
