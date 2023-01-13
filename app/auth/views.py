from flask import render_template, redirect, url_for, flash, request, make_response
from sqlalchemy.exc import SQLAlchemyError

from ..models import *
from . import auth
from _datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from ..auth.forms import LoginForm, form_add_equip, form_add_type_equip, form_add_computer, form_add_user, \
    form_add_mic, form_add_fone, form_add_webcam, form_add_monitor, form_add_call, form_edit_equip, form_edit_computer, \
    form_edit_monitor, form_edit_webcam, form_edit_fone, form_edit_mic


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
        user = User.query.filter_by(user_register=form.user.data).first()
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
            col_name = 'equip_id'
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

        if request.form.get("patrimony") == "":
            novo_equip = Equipment(
                equip_user_id=user,
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                equip_registry=datetime.today().strftime('%d/%m/%Y'),
                general_description=request.form.get("general_description"),
                type='equipments'
            )
        else:
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

        if request.form.get("patrimony") == "":
            novo_equip = Computer(
                equip_user_id=user,
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
        else:
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

        if request.form.get("patrimony") == "":
            novo_monitor = Monitor(
                equip_user_id=user,
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                model=request.form.get("model"),
                equip_registry=datetime.today().strftime('%d/%m/%Y'),
                general_description=request.form.get("general_description"),
                monitor_size=request.form.get("monitor_size"),
                monitor_resolution=request.form.get("monitor_resolution"),
                type='monitors'
            )
        else:
            novo_monitor = Monitor(
                equip_user_id=user,
                patrimony=request.form.get("patrimony"),
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                model=request.form.get("model"),
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

        if request.form.get("patrimony") == "":
            novo_webcam = WebCam(
                equip_user_id=user,
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                model=request.form.get("model"),
                equip_registry=datetime.today().strftime('%d/%m/%Y'),
                general_description=request.form.get("general_description"),
                webcam_resolution=request.form.get("webcam_resolution"),
                type='webcams'
            )
        else:
            novo_webcam = WebCam(
                equip_user_id=user,
                patrimony=request.form.get("patrimony"),
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                model=request.form.get("model"),
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

        if request.form.get("patrimony") == "":
            novo_fone = Fone(
                equip_user_id=user,
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                model=request.form.get("model"),
                equip_registry=datetime.today().strftime('%d/%m/%Y'),
                general_description=request.form.get("general_description"),
                fone_frequency=request.form.get("fone_frequency"),
                fone_impedance=request.form.get("fone_impedance"),
                fone_driver=request.form.get("fone_driver"),
                fone_noise_cancellation=request.form.get("fone_noise_cancellation"),
                type='fones'
            )
        else:
            novo_fone = Fone(
                equip_user_id=user,
                patrimony=request.form.get("patrimony"),
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                model=request.form.get("model"),
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
            novo_mic = Mic(
                equip_user_id=user,
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                equip_registry=datetime.today().strftime('%d/%m/%Y'),
                model=request.form.get("model"),
                general_description=request.form.get("general_description"),
                mic_frequency=request.form.get("mic_frequency"),
                mic_impedance=request.form.get("mic_impedance"),
                mic_noise_cancellation=request.form.get("mic_noise_cancellation"),
                type='mics'
            )
        else:
            novo_mic = Mic(
                equip_user_id=user,
                patrimony=request.form.get("patrimony"),
                brand=request.form.get("brand"),
                position=request.form.get("position"),
                equip_registry=datetime.today().strftime('%d/%m/%Y'),
                model=request.form.get("model"),
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
        lst_teams = request.form.get("user_team_id")
        novo_user = User(
            user_name=request.form.get("user_name"),
            user_register=request.form.get("user_register"),
            user_team_id=lst_teams[1],  # lst_teams é uma 'string' e não uma lista
            user_subteam_id=lst_teams[4] if len(lst_teams) == 5 else None

        )
        db.session.add(novo_user)
        # try:
        db.session.commit()
        # except SQLAlchemyError as e:
        #     db.session.rollback()
        #     error = str(e.__dict__['orig'])
        #     return render_template("auth/add_error.html", error=error, element="Usuário " + novo_user.user_name)

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


@auth.route('/call_add', methods=['POST', 'GET'])
def call_add():
    form = form_add_call()
    error = None

    if form.validate_on_submit() and request.method == "POST":
        new_call = Call(call_equipment_id=request.form.get("call_equipment"),
                        call_user_id=User.query.filter_by(user_name=request.form.get("call_user")).first().user_id,
                        call_open=datetime.now().strftime("%d/%b/%y %H:%M:%S"),
                        )
        db.session.add(new_call)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return render_template("auth/add_error.html", error=error, element="Chamado em " + new_call.call_open)

        return render_template("auth/add_success.html", title="Chamado")
    elif request.method == "POST":
        error = "problema ao criar chamado!!"

    return render_template("auth/add_call.html", form=form, error=error)


@auth.route('/edit_item/<id_equip>', methods=['POST', 'GET'])
def edit_item(id_equip):
    equip_to_edit = Equipment.query.filter_by(equip_id=id_equip).first()

    if equip_to_edit.type == 'equipments':
        form_class = form_edit_equip(equip_to_edit)
        form = form_class()
        if form.validate_on_submit() and request.method == 'POST' and current_user.is_admin():
            try:
                equip_to_edit.equip_user_id = request.form.getlist("equip_user"),
                equip_to_edit.patrimony = request.form.get("patrimony"),
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
    elif equip_to_edit.type == 'computers':
        form = form_edit_computer(equip_to_edit)
        if form.validate_on_submit() and request.method == 'POST' and current_user.is_admin():
            try:
                equip_to_edit.equip_user_id = request.form.getlist("equip_user"),
                equip_to_edit.patrimony = request.form.get("patrimony"),
                equip_to_edit.brand = request.form.get("brand"),
                equip_to_edit.position = request.form.get("position"),
                equip_to_edit.model = request.form.get("model"),
                equip_to_edit.general_description = request.form.get("general_description"),
                equip_to_edit.computer_name = request.form.get("computer_name"),
                equip_to_edit.computer_cpu = request.form.get("computer_cpu"),
                equip_to_edit.computer_so = request.form.get("computer_so"),
                equip_to_edit.computer_bios = request.form.get("computer_bios"),
                equip_to_edit.computer_memory = request.form.get("computer_memory"),
                equip_to_edit.computer_hd = request.form.get("computer_hd"),
                equip_to_edit.computer_vga = request.form.get("computer_vga"),
                equip_to_edit.computer_macaddress = request.form.get("computer_macaddress"),
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                error = str(e.__dict__['orig'])
                return render_template("auth/add_error.html", error=error)
            return render_template("auth/edit_success.html", title="Equipamento Editado")
        return render_template("auth/edit_computer.html", form=form, equip_to_edit=equip_to_edit.equip_id)
    elif equip_to_edit.type == 'monitors':
        form = form_edit_monitor(equip_to_edit)
        if form.validate_on_submit() and request.method == 'POST' and current_user.is_admin():
            user = User.query.filter_by(user_id=request.form.getlist("equip_user")[0]).first().user_id
            try:
                equip_to_edit.equip_user_id = request.form.getlist("equip_user"),
                equip_to_edit.patrimony = request.form.get("patrimony"),
                equip_to_edit.brand = request.form.get("brand"),
                equip_to_edit.position = request.form.get("position"),
                equip_to_edit.model = request.form.get("model"),
                equip_to_edit.general_description = request.form.get("general_description"),
                equip_to_edit.monitor_size = request.form.get("monitor_size"),
                equip_to_edit.monitor_resolution = request.form.get("monitor_resolution"),
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                error = str(e.__dict__['orig'])
                return render_template("auth/add_error.html", error=error)
            return render_template("auth/edit_success.html", title="Monitor Editado")
        return render_template("auth/edit_monitor.html", form=form, equip_to_edit=equip_to_edit.equip_id)
    elif equip_to_edit.type == 'webcams':
        form = form_edit_webcam(equip_to_edit)
        if form.validate_on_submit() and request.method == 'POST' and current_user.is_admin():
            try:
                equip_to_edit.equip_user_id = request.form.getlist("equip_user"),
                equip_to_edit.patrimony = request.form.get("patrimony"),
                equip_to_edit.brand = request.form.get("brand"),
                equip_to_edit.position = request.form.get("position"),
                equip_to_edit.model = request.form.get("model"),
                equip_to_edit.general_description = request.form.get("general_description"),
                equip_to_edit.webcam_resolution = request.form.get("webcam_resolution"),
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                error = str(e.__dict__['orig'])
                return render_template("auth/add_error.html", error=error)
            return render_template("auth/edit_success.html", title="WebCam Editada")
        return render_template("auth/edit_webcam.html", form=form, equip_to_edit=equip_to_edit.equip_id)
    elif equip_to_edit.type == 'fones':
        form = form_edit_fone(equip_to_edit)
        if form.validate_on_submit() and request.method == 'POST' and current_user.is_admin():
            try:
                equip_to_edit.equip_user_id = request.form.getlist("equip_user"),
                equip_to_edit.patrimony = request.form.get("patrimony"),
                equip_to_edit.brand = request.form.get("brand"),
                equip_to_edit.position = request.form.get("position"),
                equip_to_edit.model = request.form.get("model"),
                equip_to_edit.general_description = request.form.get("general_description"),
                equip_to_edit.fone_frequency = request.form.get("fone_frequency"),
                equip_to_edit.fone_driver = request.form.get("fone_driver"),
                equip_to_edit.fone_impedance = request.form.get("fone_impedance "),
                equip_to_edit.fone_noise_cancellation = request.form.get("fone_noise_cancellation"),
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                error = str(e.__dict__['orig'])
                return render_template("auth/add_error.html", error=error)
            return render_template("auth/edit_success.html", title="Fone Editado")
        return render_template("auth/edit_fone.html", form=form, equip_to_edit=equip_to_edit.equip_id)
    elif equip_to_edit.type == 'mics':
        form = form_edit_mic(equip_to_edit)
        if form.validate_on_submit() and request.method == 'POST' and current_user.is_admin():
            try:
                equip_to_edit.equip_user_id = request.form.getlist("equip_user"),
                equip_to_edit.patrimony = request.form.get("patrimony"),
                equip_to_edit.brand = request.form.get("brand"),
                equip_to_edit.position = request.form.get("position"),
                equip_to_edit.model = request.form.get("model"),
                equip_to_edit.general_description = request.form.get("general_description"),
                equip_to_edit.mic_frequency = request.form.get("mic_frequency"),
                equip_to_edit.mic_impedance = request.form.get("mic_impedance"),
                equip_to_edit.mic_noise_cancellation = request.form.get("mic_noise_cancellation"),
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                error = str(e.__dict__['orig'])
                return render_template("auth/add_error.html", error=error)
            return render_template("auth/edit_success.html", title="Microfone Editado")
        return render_template("auth/edit_mic.html", form=form, equip_to_edit=equip_to_edit.equip_id)
    else:
        return "Error line 1053 views"


@auth.route('/detail_item/<id_equip>', methods=['POST', 'GET'])
def detail_item(id_equip):
    equip_detail = Equipment.query.filter_by(equip_id=id_equip).first()

    if equip_detail.type == "equipments":
        return render_template("auth/detail_equip.html", equip_detail=equip_detail)
    elif equip_detail.type == "computers":
        return render_template("auth/detail_computer.html", equip_detail=equip_detail)
    elif equip_detail.type == "monitors":
        return render_template("auth/detail_monitor.html", equip_detail=equip_detail)
    elif equip_detail.type == "webcams":
        return render_template("auth/detail_webcam.html", equip_detail=equip_detail)
    elif equip_detail.type == "fones":
        return render_template("auth/detail_fone.html", equip_detail=equip_detail)
    elif equip_detail.type == "mics":
        return render_template("auth/detail_mic.html", equip_detail=equip_detail)