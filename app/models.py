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
    equip_registry = db.Column(db.String(64))  # data que o resgitro foi criado
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
    computer_id = db.Column(db.Integer, db.ForeignKey('equipments.equip_id', ondelete='CASCADE'), primary_key=True)
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
            'computer_id': self.equip_id,
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
    call_technican = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, server_default="0")
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


class SubTeam(db.Model):
    __tablename__ = "subteams"
    subteam_team_id = db.Column(db.ForeignKey("teams.team_id"))
    subteam_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    subteam_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Nome %r>' % self.subteam_name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_register = db.Column(db.String(64), nullable=True)
    user_name = db.Column(db.String(64), nullable=False)
    user_pass = db.Column(db.String(64), nullable=False, server_default="Dia 2 de fevereiro é o dia mais lindo que há")
    user_equipments = db.relationship("Equipment", backref="users")
    user_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    user_subteam_id = db.Column(db.Integer, db.ForeignKey('subteams.subteam_id'), nullable=True)

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
        get_subteam_name = self.user_subteam_id

        if get_subteam_name is not None:
            get_subteam_name = SubTeam.query.filter(SubTeam.subteam_id == self.user_subteam_id).first().subteam_name

        return {
            'user_id': self.user_id,
            'user_register': self.user_register,
            'user_name': self.user_name,
            'user_team_id': Team.query.filter(Team.team_id == self.user_team_id).first().team_name,
            'user_subteam_id': get_subteam_name

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
    db.session.add(Team(team_id=1, team_name="Gabinete", team_leader="Maria Josele Bucco Coelho"))
    db.session.add(Team(team_id=2, team_name="COPEG", team_leader="Maria Tereza Carneiro Soares"))
    db.session.add(Team(team_id=3, team_name="COPAC", team_leader="Eliane Felisbino"))
    db.session.add(Team(team_id=4, team_name="COPAP", team_leader="José Carlos Eidam"))
    db.session.add(Team(team_id=5, team_name="COAFE", team_leader="Leonir Lorenzetti"))
    db.session.add(Team(team_id=6, team_name="COSIS", team_leader="Rafaela Mantovani Fontana"))
    db.session.add(Team(team_id=7, team_name="CIPEAD", team_leader="Geovana Gentili Santos"))
    db.session.add(Team(team_id=8, team_name="NC", team_leader="Alexandre Trovon de Carvalho"))
    db.session.commit()


@event.listens_for(SubTeam.__table__, 'after_create')
def insert_initial_values2(*args, **kwargs):
    db.session.add(SubTeam(subteam_id=1, subteam_team_id=1, subteam_name="Financeiro"))
    db.session.add(SubTeam(subteam_id=2, subteam_team_id=1, subteam_name="Secretaria"))
    db.session.add(SubTeam(subteam_id=3, subteam_team_id=4, subteam_name="Seção de Acompanhamento Acadêmico (SAAC)"))
    db.session.add(SubTeam(subteam_id=4, subteam_team_id=4, subteam_name="Seção de Gerenciamento Acadêmico (SGA)"))
    db.session.add(SubTeam(subteam_id=5, subteam_team_id=4, subteam_name="Unidade de Diplomas (UD)"))
    db.session.add(SubTeam(subteam_id=6, subteam_team_id=4, subteam_name="Seção de Ocupação de Vaga (SOCV)"))
    db.session.add(SubTeam(subteam_id=7, subteam_team_id=5, subteam_name="Unidade de Estágios (UE)"))
    db.session.add(SubTeam(subteam_id=8, subteam_team_id=5, subteam_name="Unidades de Atividades Formativas (UAF)"))
    db.session.add(SubTeam(subteam_id=9, subteam_team_id=7, subteam_name="Unidade Administrativa"))
    db.session.add(SubTeam(subteam_id=10, subteam_team_id=7, subteam_name="Unidade Pedagógica"))
    db.session.add(SubTeam(subteam_id=11, subteam_team_id=7, subteam_name="LabCIPEAD"))
    db.session.add(SubTeam(subteam_id=12, subteam_team_id=7, subteam_name="Equipe Multidisciplinar"))
    db.session.commit()


@event.listens_for(User.__table__, 'after_create')
def insert_initial_values3(*ars, **kwargs):
    db.session.add(User(user_register="1",
                        user_name="Jaqueline Cavalari Sales de Almeida", user_team_id=1, user_subteam_id=1))
    db.session.add(User(user_register="2",
                        user_name="Cristiano Rodrigues Amorim", user_team_id=1, user_subteam_id=1))
    db.session.add(User(user_register="3",
                        user_name="Isaque Moraes dos Santos", user_team_id=1, user_subteam_id=1))
    db.session.add(User(user_register="4",
                        user_name="Mariane de Siqueira", user_team_id=1, user_subteam_id=2))
    db.session.add(User(user_register="5",
                        user_name="Luana Moraes Costa", user_team_id=2))
    db.session.add(User(user_register="6",
                        user_name="Paulo Feres Bockor", user_team_id=3))
    db.session.add(User(user_register="7",
                        user_name="Tommaso Lilli", user_team_id=3))
    db.session.add(User(user_register="8",
                        user_name="Viviane Vidal Pereira dos Santos", user_team_id=3))
    db.session.add(User(user_register="9", user_name="Gislaine Pereira Ramos", user_team_id=4, user_subteam_id=3))
    db.session.add(User(user_register="10", user_name="Isabelle Aparecida Borges", user_team_id=4, user_subteam_id=3))
    db.session.add(User(user_register="11", user_name="Evaldo Amaral", user_team_id=4, user_subteam_id=4))
    db.session.add(User(user_register="12",
                        user_name="Laysla Fernanda Silva Viveiros", user_team_id=4, user_subteam_id=4))
    db.session.add(User(user_register="13", user_name="Tatyane Nunes", user_team_id=4, user_subteam_id=4))
    db.session.add(User(user_register="14",
                        user_name="Valéria da Silva Leite Ravanello", user_team_id=4, user_subteam_id=4))
    db.session.add(User(user_register="15",
                        user_name="Leonilda Ianckievicz Pacheco de Andrade", user_team_id=4, user_subteam_id=5))
    db.session.add(User(user_register="16", user_name="Luciano Vans", user_team_id=4, user_subteam_id=5))
    db.session.add(User(user_register="17", user_name="Marco Antonio Weber Jorge", user_team_id=4, user_subteam_id=5))
    db.session.add(User(user_register="18", user_name="Simone Aparecida Verchai", user_team_id=4, user_subteam_id=5))
    db.session.add(User(user_register="19",
                        user_name="Kelly Cristine Schibelbain Santos", user_team_id=4, user_subteam_id=5))
    db.session.add(User(user_register="20", user_name="Wender Ribeiro", user_team_id=4, user_subteam_id=5))
    db.session.add(User(user_register="21",
                        user_name="Adriana Cristina Wasuaski Riechter", user_team_id=4, user_subteam_id=6))
    db.session.add(User(user_register="22", user_name="Lairdes Figueredo Cheke", user_team_id=4, user_subteam_id=6))
    db.session.add(User(user_register="23",
                        user_name="Gina Marcela Marcassi Rodrigues de Lima", user_team_id=4, user_subteam_id=6))
    db.session.add(User(user_register="24", user_name="Flavia Vieira", user_team_id=4, user_subteam_id=6))
    db.session.add(User(user_register="25", user_name="Tânia Lazier Gabardo", user_team_id=5, user_subteam_id=7))
    db.session.add(User(user_register="26", user_name="Eliane Cristina Depetris", user_team_id=5, user_subteam_id=7))
    db.session.add(User(user_register="27", user_name="Franciane Retslaff", user_team_id=5, user_subteam_id=7))
    db.session.add(User(user_register="28",
                        user_name="Jocimara Rodrigues Cardoso dos Santos", user_team_id=5, user_subteam_id=7))
    db.session.add(User(user_register="29", user_name="Paulo César de Freitas", user_team_id=5, user_subteam_id=7))
    db.session.add(User(user_register="30", user_name="Laura Somoza", user_team_id=5, user_subteam_id=8))
    db.session.add(User(user_register="31", user_name="Eversong Paulo Zuba", user_team_id=5, user_subteam_id=8))
    db.session.add(User(user_register="32", user_name="Bruna Coutrim de Oliveira", user_team_id=5, user_subteam_id=8))
    db.session.add(User(user_register="33", user_name="Cesar Augustus Akatsu", user_team_id=6))
    db.session.add(User(user_register="34", user_name="Me. Josemar Pereira da Silva", user_team_id=6))
    db.session.add(User(user_register="35", user_name="Kleyton Lucas de Souza", user_team_id=6))
    db.session.add(User(user_register="36", user_name="Lorena Kruger", user_team_id=6))
    db.session.add(User(user_register="37",
                        user_name="Rafael Casale Sartor de Oliveira ", user_team_id=7, user_subteam_id=9))
    db.session.add(User(user_register="38",
                        user_name="Naia Paula Yolanda Bittencourt Tortato", user_team_id=7, user_subteam_id=9))
    db.session.add(User(user_register="39", user_name="Anna Jungbluth", user_team_id=7, user_subteam_id=10))
    db.session.add(User(user_register="40", user_name="Marina Lupepso", user_team_id=7, user_subteam_id=10))
    db.session.add(User(user_register="41",
                        user_name="Tatiana Raquel Baptista Greff", user_team_id=7, user_subteam_id=10))
    db.session.add(User(user_register="42", user_name="Elizabete Gomes", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="43",
                        user_name="Erick Martins do Nascimento", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="44",
                        user_name="Lucas Vinicius Vebber Caroenas", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="45",
                        user_name="Fernanda Cristina Dalazen Fernandes", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="46",
                        user_name="Piero Enrico Ribas Salamone", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="47",
                        user_name="Gabriely Woiciekowski Colares", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="47",
                        user_name="Tacila Fernanda Carneiro Evangelhista", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="48", user_name="Fabiano Francisco Amaral", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="50", user_name="Rodrigo Dittmar", user_team_id=7, user_subteam_id=11))
    db.session.add(User(user_register="51",
                        user_name="Ana Carolina de Araújo Silva", user_team_id=7, user_subteam_id=12))
    db.session.add(User(user_register="52", user_name="Celso Yoshikazu Ishida", user_team_id=7, user_subteam_id=12))
    db.session.add(User(user_register="53", user_name="Geovana Gentili Santos", user_team_id=7, user_subteam_id=12))
    db.session.add(User(user_register="54",
                        user_name="Kelly Priscilla Loddo Cezar", user_team_id=7, user_subteam_id=12))
    db.session.commit()
