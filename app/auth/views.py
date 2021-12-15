import requests
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy.exc import SQLAlchemyError

from ..models import *
from . import auth
from _datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from ..auth.forms import LoginForm, form_add_equip, form_add_type_equip, form_add_computer, form_add_user, \
    form_add_mic, form_add_fone, form_add_webcam, form_add_monitor


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
        flash("Faça login para acessar os dados.", 'cad')
    return render_template('auth/login.html', form=form)


@login_required
@auth.route('/equips_list', methods=['GET', 'POST'])
def equips_list():
    # equipments = Equipment.query
    return render_template('auth/equips_list.html')  # , equipments=equipments)


@login_required
@auth.route('/monitors_list', methods=['GET', 'POST'])
def monitors_list():
    # monitors = Monitor.query
    return render_template('auth/monitors_list.html')  # , monitors=monitors)


@login_required
@auth.route('/fones_list', methods=['GET', 'POST'])
def fones_list():
    # fones = Monitor.query
    return render_template('auth/fones_list.html')  # , fones=fones)


@login_required
@auth.route('/mics_list', methods=['GET', 'POST'])
def mics_list():
    # mics = Mic.query
    return render_template('auth/mics_list.html')  # , mics=mics)


@login_required
@auth.route('/webcams_list', methods=['GET', 'POST'])
def webcams_list():
    # webcams = WebCam.query
    return render_template('auth/webcams_list.html')  # , webcams=webcams)


@login_required
@auth.route('/computers_list', methods=['GET', 'POST'])
def computers_list():
    # computers = Computer.query
    return render_template('auth/computers_list.html')  # , computers=computers)


@login_required
@auth.route('/users_list', methods=['GET', 'POST'])
def users_list():
    # users = User.query
    return render_template('auth/users_list.html')  # , users=users)


@login_required
@auth.route('/calls_list', methods=['GET', 'POST'])
def calls_list():
    # calls = Call.query
    return render_template('auth/calls_list.html')  # , calls=calls)


@auth.route('/api/equips')
def equips_data():
    query = Equipment.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(Equipment).join(User).filter(db.or_(
            Equipment.patrimony.like(f'%{search}%'),
            Equipment.type.like(f'%{search}%'),
            Equipment.brand.like(f'%{search}%'),
            User.user_name.like(f'%{search}%')
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
            User.user_name.like(f'%{search}%'),
            User.user_register.like(f'%{search}%'),
            Team.team_name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        print(col_name)
        if col_name not in ['user_id', 'user_register', 'user_name', 'user_team_id', 'user_subteam_id']:
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
        query = db.session.query(Call).join(User).filter(db.or_(
            Call.call_open.like(f'%{search}%'),
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


@auth.route('/api/monitors')
def monitors_data():
    query = Monitor.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(Monitor).join(User).filter(db.or_(
            Monitor.patrimony.like(f'%{search}%'),
            Monitor.monitor_size.like(f'%{search}%'),
            Monitor.brand.like(f'%{search}%'),
            User.user_name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['monitor_id', 'monitor_user', 'patrimony', 'model', 'brand', 'monitor_size']:
            col_name = 'equip_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Monitor, col_name)
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

    return {
        'data': [monitor.to_dict() for monitor in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Monitor.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/api/computers')
def computers_data():
    query = Computer.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(Computer).join(User).filter(db.or_(
            Computer.patrimony.like(f'%{search}%'),
            Computer.computer_hd.like(f'%{search}%'),
            Computer.computer_memory.like(f'%{search}%'),
            Computer.brand.like(f'%{search}%'),
            Computer.model.like(f'%{search}%'),
            Computer.computer_name.like(f'%{search}%'),
            Computer.computer_so.like(f'%{search}%'),
            Computer.computer_cpu.like(f'%{search}%'),
            Computer.patrimony.like(f'%{search}%'),
            User.user_name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['computer_id', 'model', 'computer_user', 'computer_name',
                            'computer_so', 'brand', 'computer_cpu', 'computer_memory']:
            col_name = 'computer_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Computer, col_name)
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
        'data': [computer.to_dict() for computer in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Computer.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/api/fones')
def fones_data():
    query = Fone.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(Fone).join(User).filter(db.or_(
            Fone.patrimony.like(f'%{search}%'),
            Fone.brand.like(f'%{search}%'),
            Fone.fone_driver.like(f'%{search}%'),
            Fone.fone_frequency.like(f'%{search}%'),
            Fone.all_connections.like(f'%{search}%'),
            User.user_name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['fone_id', 'fone_user', 'fone_driver', 'brand',
                            'model', 'fone_frequency', 'fone_impedance', 'fone_noise_cancellation']:
            col_name = 'fone_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Fone, col_name)
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
        'data': [fone.to_dict() for fone in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Fone.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/api/mics')
def mics_data():
    query = Mic.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(Mic).join(User).filter(db.or_(
            Mic.patrimony.like(f'%{search}%'),
            Mic.mic_frequency.like(f'%{search}%'),
            Mic.mic_noise_cancellation.like(f'%{search}%'),
            Mic.mic_impedance.like(f'%{search}%'),
            User.user_name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['mic_id', 'mic_user', 'mic_frequency', 'brand',
                            'mic_noise_cancellation', 'mic_impedance', 'patrimony', 'mic_model']:
            col_name = 'mic_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Mic, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    print(12)
    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response

    return {
        'data': [mic.to_dict() for mic in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Mic.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/api/webcams')
def webcams_data():
    query = WebCam.query

    search = request.args.get('search[value]')
    if search:
        query = db.session.query(Monitor).join(User).filter(db.or_(
            WebCam.patrimony.like(f'%{search}%'),
            WebCam.brand.like(f'%{search}%'),
            WebCam.webcam_resolution.like(f'%{search}%'),
            User.user_name.like(f'%{search}%')
        ))

    total_filtered = query.count()

    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['webcam_id', 'webcam_user', 'patrimony', 'webcam_resolution', 'brand', 'model',
                            'equip_registry']:
            col_name = 'webcam_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(WebCam, col_name)
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
        'data': [webcam.to_dict() for webcam in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': WebCam.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@auth.route('/choose_equip_type', methods=['GET', 'POST'])
def choose_equip_type():
    type_equips = [cls.__name__ for cls in Equipment.__subclasses__()]

    type_equips.append("Equipment")

    form = form_add_type_equip()

    form.type.choices = type_equips

    if form.validate_on_submit() and request.method == 'POST':
        if request.form.get("type") == "Equipment":
            return redirect(url_for("auth.add_equip"))
        elif request.form.get("type") == "Computer":
            return redirect(url_for("auth.add_computer"))
        elif request.form.get("type") == "Monitor":
            return redirect(url_for("auth.add_monitor"))
        elif request.form.get("type") == "WebCam":
            return redirect(url_for("auth.add_webcam"))
        elif request.form.get("type") == "Fone":
            return redirect(url_for("auth.add_fone"))
        elif request.form.get("type") == "Mic":
            return redirect(url_for("auth.add_mic"))
        else:
            return '<h1 class="btn btn-danger">Erro! Tipo de Equipamento não encontrado!</h1>'

    if request.method == 'POST':
        flash('Preenchimento Obrigatório!', 'fill')
        return redirect(url_for("auth.choose_equip_type"))

    return render_template("auth/equip_add_choose_type.html", type_equips=type_equips, form=form)


# @auth.route('/add_equip/<type>', methods=['GET'])
# @auth.route('/add_equip', methods=['POST'], defaults={'type': None})
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
        user = User.query.filter_by(user_id=request.form.getlist("equip_user")[0]).first().user_id
        novo_equip = Equipment(
            equip_user_id=user,
            patrimony=request.form.get("patrimony"),
            brand=request.form.get("brand"),
            position=request.form.get("position"),
            equip_registry=datetime.today().strftime('%d/%m/%Y'),
            general_description=request.form.get("general_description"),
            type='equipments'
        )
        db.session.add(novo_equip)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)

        return render_template("auth/add_success.html", title="Equipamento Genérico")

    return render_template("auth/add_equip.html", form=form) \
 \
        # @auth.route('/add_computer/<type>', methods=['GET'])


@auth.route('/add_computer', methods=['POST', 'GET'])
def add_computer():
    # classes_equips_list = Equipment.__subclasses__()
    # classes_equips_list.append(Equipment)
    #
    # for name_classe in classes_equips_list:
    #     if name_classe.__name__ == type:
    #         # form.fields.choices = name_classe.__table__.columns.keys()
    #         return render_template("auth/add_equip.html", form=form)

    form = form_add_computer()

    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(user_id=request.form.getlist("equip_user")[0]).first().user_id
        novo_equip = Computer(
            equip_user_id=user,
            patrimony=request.form.get("patrimony"),
            brand=request.form.get("brand"),
            position=request.form.get("position"),
            computer_name=request.form.get("computer_name"),
            equip_registry=datetime.today().strftime('%d/%m/%Y'),
            general_description=request.form.get("general_description"),
            computer_cpu=request.form.get("computer_cpu"),
            computer_so=request.form.get("computer_so"),
            computer_bios=request.form.get("computer_bios"),
            computer_memory=request.form.get("computer_memory"),
            computer_hd=request.form.get("computer_hd"),
            computer_vga=request.form.get("computer_vga"),
            computer_macaddress=request.form.get("computer_macaddress"),
            computer_capacity_memory=request.form.get("computer_capacity_memory"),
            type='computers'
        )
        db.session.add(novo_equip)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)

        return render_template("auth/add_success.html", title="Computador ")

    return render_template("auth/add_computer.html", form=form)


@auth.route('/add_monitor', methods=['POST', 'GET'])
def add_monitor():
    # classes_equips_list = Equipment.__subclasses__()
    # classes_equips_list.append(Equipment)
    #
    # for name_classe in classes_equips_list:
    #     if name_classe.__name__ == type:
    #         # form.fields.choices = name_classe.__table__.columns.keys()
    #         return render_template("auth/add_equip.html", form=form)

    form = form_add_monitor()

    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(user_id=request.form.getlist("equip_user")[0]).first().user_id
        novo_monitor = Monitor(
            equip_user_id=user,
            patrimony=request.form.get("patrimony"),
            brand=request.form.get("brand"),
            position=request.form.get("position"),
            equip_registry=datetime.today().strftime('%d/%m/%Y'),
            general_description=request.form.get("general_description"),
            monitor_size=request.form.get("monitor_size"),
            monitor_resolution=request.form.get("monitor_resolution"),
            type='monitors'
        )
        db.session.add(novo_monitor)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)

        return render_template("auth/add_success.html", title="Monitor ")

    return render_template("auth/add_monitor.html", form=form)


@auth.route('/add_webcam', methods=['POST', 'GET'])
def add_webcam():
    # classes_equips_list = Equipment.__subclasses__()
    # classes_equips_list.append(Equipment)
    #
    # for name_classe in classes_equips_list:
    #     if name_classe.__name__ == type:
    #         # form.fields.choices = name_classe.__table__.columns.keys()
    #         return render_template("auth/add_equip.html", form=form)

    form = form_add_webcam()

    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(user_id=request.form.getlist("equip_user")[0]).first().user_id
        novo_webcam = WebCam(
            equip_user_id=user,
            patrimony=request.form.get("patrimony"),
            brand=request.form.get("brand"),
            position=request.form.get("position"),
            equip_registry=datetime.today().strftime('%d/%m/%Y'),
            general_description=request.form.get("general_description"),
            webcam_resolution=request.form.get("webcam_resolution"),
            type='webcams'
        )
        db.session.add(novo_webcam)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)

        return render_template("auth/add_success.html", title="Webcam ")

    return render_template("auth/add_webcam.html", form=form)


@auth.route('/add_fone', methods=['POST', 'GET'])
def add_fone():
    # classes_equips_list = Equipment.__subclasses__()
    # classes_equips_list.append(Equipment)
    #
    # for name_classe in classes_equips_list:
    #     if name_classe.__name__ == type:
    #         # form.fields.choices = name_classe.__table__.columns.keys()
    #         return render_template("auth/add_equip.html", form=form)

    form = form_add_fone()

    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(user_id=request.form.getlist("equip_user")[0]).first().user_id
        novo_fone = Fone(
            equip_user_id=user,
            patrimony=request.form.get("patrimony"),
            brand=request.form.get("brand"),
            position=request.form.get("position"),
            equip_registry=datetime.today().strftime('%d/%m/%Y'),
            general_description=request.form.get("general_description"),
            fone_frequency=request.form.get("fone_frequency"),
            fone_impedance=request.form.get("fone_impedance"),
            fone_driver=request.form.get("fone_driver"),
            fone_noise_cancellation=request.form.get("fone_noise_cancellation"),
            type='fones'
        )
        db.session.add(novo_fone)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)

        return render_template("auth/add_success.html", title="Fone ")

    return render_template("auth/add_fone.html", form=form)


@auth.route('/add_mic', methods=['POST', 'GET'])
def add_mic():
    # classes_equips_list = Equipment.__subclasses__()
    # classes_equips_list.append(Equipment)
    #
    # for name_classe in classes_equips_list:
    #     if name_classe.__name__ == type:
    #         # form.fields.choices = name_classe.__table__.columns.keys()
    #         return render_template("auth/add_equip.html", form=form)
    form = form_add_mic()

    if form.validate_on_submit() and request.method == 'POST':

        user = User.query.filter_by(user_id=request.form.getlist("equip_user")[0]).first().user_id

        if request.form.get("patrimony") == "":
            patrimony = None
        else:
            patrimony = request.form.get("patrimony")

        novo_mic = Mic(
            equip_user_id=user,
            patrimony=patrimony,
            brand=request.form.get("brand"),
            position=request.form.get("position"),
            equip_registry=datetime.today().strftime('%d/%m/%Y'),
            general_description=request.form.get("general_description"),
            mic_frequency=request.form.get("mic_frequency"),
            mic_impedance=request.form.get("mic_impedance"),
            mic_noise_cancellation=request.form.get("mic_noise_cancellation"),
            type='mics'
        )
        db.session.add(novo_mic)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)

        return render_template("auth/add_success.html", title="Mic ")
    return render_template("auth/add_mic.html", form=form)


@auth.route('/user_add', methods=['POST', 'GET'])
def user_add():
    form = form_add_user()

    if form.validate_on_submit() and request.method == 'POST':

        novo_user = User(
            user_name=request.form.get("user_name"),
            user_register=request.form.get("user_register"),
            user_team_id=request.form.getlist("user_team_id")[0],
            user_subteam_id=request.form.getlist("user_team_id")[1],

        )
        db.session.add(novo_user)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error)

        return render_template("auth/add_success.html", title="Novo Usuário")

    return render_template("auth/add_user.html", form=form)


@auth.route('/call_add')
def call_add():
    return "add_user"
