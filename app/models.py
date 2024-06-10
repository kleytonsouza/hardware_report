from . import db, login_manager
from flask_login import UserMixin
from sqlalchemy import DDL, event


class Equipment(db.Model):
    __tablename__ = "equipments"
    equip_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    equip_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    patrimony = db.Column(db.String(64), nullable=True, unique=True)
    brand = db.Column(db.String(64), nullable=True)
    model = db.Column(db.String(64), nullable=True)
    position = db.Column(db.String(64), nullable=True)
    equip_registry = db.Column(db.String(64))  # data que o registro foi criado
    general_description = db.Column(db.String(64), nullable=True)
    type = db.Column(db.String(64), nullable=True)
    all_calls = db.relationship("Call", backref="equipments")
    all_connections = db.relationship("EquipmentConnection", backref="equipments")

    def equip_to_dict(self):
        return {
            'equip_id': self.equip_id,
            'equip_user_id': User.query.filter(User.user_id == self.equip_user_id).first().user_name,
            'patrimony': self.patrimony,
            'brand': self.brand,
            'model': self.model,
            'equip_registry': self.equip_registry,
            # 'general_description': self.general_description,
            'type': self.type

        }

    def __repr__(self):
        return str(self.equip_id)

    def is_admin(self):
        admin = Admin.query.filter(Admin.user_id == self.equip_user_id).first()
        if admin is not None:
            return True
        else:
            return False

    # def edit_equip(self):
    #     equip_new = Equipment.query.filter(Equipment.equip_id == self.equip_id).first()
    #     db.session.add(equip_new)
    #     db.session.commit()

    __mapper_args__ = {
        'polymorphic_identity': 'equipments',
        'polymorphic_on': type
    }

    # __table_args__ = (
    #     db.UniqueConstraint(
    #         patrimony),
    # )


class Computer(Equipment):
    __tablename__ = "computers"
    __mapper_args__ = {'polymorphic_identity': 'computers'}
    # computer_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id', ondelete='CASCADE'), primary_key=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id'), primary_key=True)
    computer_name = db.Column(db.String(64), nullable=False, unique=True)
    computer_cpu = db.Column(db.String(64))
    computer_so = db.Column(db.String(64))
    computer_bios = db.Column(db.String(64))
    computer_memory = db.Column(db.String(64))
    computer_hd = db.Column(db.String(64))
    computer_vga = db.Column(db.String(64))
    computer_macaddress = db.Column(db.String(64))
    computer_capacity_memory = db.Column(db.String(64))
    computer_storages = db.relationship("Storage", backref="computers")

    def to_dict(self):
        return {
            'computer_id': self.computer_id,
            'computer_user': User.query.filter(User.user_id == self.equip_user_id).first().user_name,
            'computer_name': self.computer_name,
            'patrimony': self.patrimony,
            'brand': self.brand,
            'model': self.model,
            'computer_cpu': self.computer_cpu,
            'computer_memory': self.computer_memory,
            'computer_hd': self.computer_hd,
            'computer_macaddress': self.computer_macaddress,
            'computer_so': self.computer_so

        }


class Storage(db.Model):
    __tablename__ = "storages"
    storage_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id'), primary_key=True)
    storage_name = db.Column(db.String(64))
    storage_size = db.Column(db.String(64), nullable=False)
    storage_type = db.Column(db.String(64))
    storage_computer = db.Column(db.Integer, db.ForeignKey('computers.computer_id'), nullable=True)
    # computer_ip = db.Column(db.String(64))


class Monitor(Equipment):
    __tablename__ = "monitors"
    __mapper_args__ = {'polymorphic_identity': 'monitors'}
    monitor_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id'), primary_key=True)
    monitor_size = db.Column(db.String(64))
    monitor_resolution = db.Column(db.String(64))

    def to_dict(self):
        return {
            'monitor_id': self.monitor_id,
            'monitor_user': User.query.filter(User.user_id == self.equip_user_id).first().user_name,
            'patrimony': self.patrimony,
            'brand': self.brand,
            'model': self.model,
            'equip_registry': self.equip_registry,
            'monitor_size': self.monitor_size,
            'monitor_resolution': self.monitor_resolution
        }


class WebCam(Equipment):
    __tablename__ = "webcams"
    __mapper_args__ = {'polymorphic_identity': 'webcams'}
    webcam_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id'), primary_key=True)
    webcam_resolution = db.Column(db.String(64))

    def to_dict(self):
        return {
            'webcam_id': self.equip_id,
            'webcam_user': User.query.filter(User.user_id == self.equip_user_id).first().user_name,
            'patrimony': self.patrimony,
            'brand': self.brand,
            'model': self.model,
            'equip_registry': self.equip_registry,
            'webcam_resolution': self.webcam_resolution
        }


class Fone(Equipment):
    __tablename__ = "fones"
    __mapper_args__ = {'polymorphic_identity': 'fones'}
    fone_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id'), primary_key=True)
    fone_frequency = db.Column(db.String(64), nullable=True)
    fone_impedance = db.Column(db.String(64), nullable=True)
    fone_driver = db.Column(db.String(64), nullable=True)
    fone_noise_cancellation = db.Column(db.String(64), nullable=True)

    # fone_mic = db.Column(db.Integer, db.ForeignKey('mics.mic_id'), nullable=True)

    def to_dict(self):
        return {
            'fone_id': self.fone_id,
            'fone_frequency': self.fone_frequency,
            'fone_impedance': self.fone_impedance,
            'fone_noise_cancellation': self.fone_noise_cancellation,
            'fone_driver': self.fone_driver,
            'fone_user': User.query.filter(User.user_id == self.equip_user_id).first().user_name,
            'patrimony': self.patrimony,
            'brand': self.brand,
            'model': self.model,
            'equip_registry': self.equip_registry,
        }


class Mic(Equipment):
    __tablename__ = "mics"
    __mapper_args__ = {'polymorphic_identity': 'mics'}
    mic_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id'), primary_key=True)
    mic_noise_cancellation = db.Column(db.String(64))
    mic_frequency = db.Column(db.String(64))
    mic_impedance = db.Column(db.String(64))

    def to_dict(self):
        return {
            'mic_id': self.mic_id,
            'mic_noise_cancellation': self.mic_noise_cancellation,
            'mic_frequency': self.mic_frequency,
            'mic_impedance': self.mic_impedance,
            'mic_user': User.query.filter(User.user_id == self.equip_user_id).first().user_name,
            'patrimony': self.patrimony,
            'brand': self.brand,
            'model': self.model,
            'equip_registry': self.equip_registry,
        }


class Call(db.Model):
    __tablename__ = "calls"
    call_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    call_equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id'), nullable=False)
    call_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    call_open = db.Column(db.String(64), nullable=False)
    call_close = db.Column(db.String(64), nullable=True)
    call_technican = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, default="0")
    call_solution = db.Column(db.String(700), nullable=True)

    def to_dict(self):
        return {
            'call_id': self.call_id,
            'call_equipment_id': self.call_equipment_id,
            'call_open': self.call_open,
            'call_close': self.call_close,
            'call_solution': self.call_solution,
            'call_user': User.query.filter(User.user_id == self.call_user_id).first().user_name,

        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Connection(db.Model):
    __tablename__ = "connections"
    connection_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    connection_name = db.Column(db.String(64))


class EquipmentConnection(db.Model):
    __tablename__ = "equipment_connetions"
    equipment = db.Column(db.Integer, db.ForeignKey('equipments.equip_id'), nullable=False, primary_key=True)
    connection = db.Column(db.Integer, db.ForeignKey('connections.connection_id'), nullable=False, primary_key=True)


class Team(db.Model):
    __tablename__ = "teams"
    team_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    team_name = db.Column(db.String(64), nullable=False)
    team_leader = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Nome %r>' % self.team_name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_register = db.Column(db.String(64), nullable=True)
    user_name = db.Column(db.String(64), nullable=False)
    user_pass = db.Column(db.String(64), nullable=False, default="Dia 2 de fevereiro é o dia mais lindo que há")
    user_equipments = db.relationship("Equipment", backref="users")
    user_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            user_register, user_name),
    )

    def is_admin(self):
        admin = Admin.query.filter(Admin.user_id == self.user_id).first()
        if admin is not None:
            return True
        else:
            return False

    @property
    def password(self):
        raise AttributeError('não é permitido ler a senha')

    def verify_password(self, password):
        if self.user_pass == password and self.user_pass is not None:
            return True
        return False

    def get_id(self):
        return self.user_id

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_dict(self):

        return {
            'user_id': self.user_id,
            'user_register': self.user_register,
            'user_name': self.user_name,
            'user_team_id': Team.query.filter(Team.team_id == self.user_team_id).first().team_name,

        }

    def __repr__(self):
        return self.user_name


class Admin(User):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    admin_name = db.Column(db.String(64), unique=True, index=True)
    #admin_pass_wd = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.admin_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()


@event.listens_for(Team.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Team(team_id=1, team_name="Smart Coffe", team_leader="Alexandre MaeSato"))
    db.session.add(Team(team_id=2, team_name="Linkin Dart", team_leader="Rodrigo"))
    db.session.add(Team(team_id=3, team_name="QA", team_leader="Diana Souza"))
    db.session.add(Team(team_id=4, team_name="Produto", team_leader="Produto"))
    db.session.add(Team(team_id=5, team_name="Generico", team_leader="Generico"))
    db.session.add(Team(team_id=6, team_name="PO", team_leader="Valeria Villaverde"))
    db.session.add(Team(team_id=7, team_name="SM", team_leader="Uriel Boscolo"))
    db.session.commit()


@event.listens_for(User.__table__, 'after_create')
def insert_initial_values3(*ars, **kwargs):
    db.session.add(User(user_register="1",
                        user_name="Alexandre Maesato", user_team_id=1))
    db.session.add(User(user_register="2",
                        user_name="Uriel Boscolo", user_team_id=7))
    db.session.add(User(user_register="3",
                        user_name="Rodrigo Knop", user_team_id=1))
    db.session.add(User(user_register="4",
                        user_name="Jean Will", user_team_id=1))
    db.session.add(User(user_register="5",
                        user_name="Altieres ", user_team_id=1))
    db.session.add(User(user_register="6",
                        user_name="Douglas Novaki", user_team_id=1))
    db.session.add(User(user_register="7",
                        user_name="Kleyton Lucas de Souza", user_team_id=1))
    db.session.add(User(user_register="8",
                        user_name="Igor Alfredo Fortti", user_team_id=1))
    db.session.add(User(user_register="9", user_name="Andrew Oliveira", user_team_id=1))
    db.session.add(User(user_register="10", user_name="Diana Souza", user_team_id=3))
    db.session.add(User(user_register="11", user_name="Sarah Silva", user_team_id=3))
    db.session.add(User(user_register="12",
                        user_name="Alessandra Silva", user_team_id=3))
    db.session.add(User(user_register="13", user_name="Nelson Gonzales", user_team_id=3))
    db.session.add(User(user_register="14",
                        user_name="Valeria VillaVerde", user_team_id=6))
    db.session.commit()
