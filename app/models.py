from flask_login import UserMixin
from sqlalchemy import event

from . import db, login_manager


class Equipment(db.Model):
    __tablename__ = "equipments"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    devid = db.Column(db.String(64), nullable=True, unique=True)
    brand = db.Column(db.String(64), nullable=True)
    model = db.Column(db.String(64), nullable=True)
    # add_for = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registry = db.Column(db.String(64))
    general_description = db.Column(db.String(64), nullable=True)
    type = db.Column(db.String(64), nullable=True)
    all_equipment_usage_history = db.relationship("EquipmentUsageHistory", backref="equipments")

    def equip_to_dict(self):
        return {
            'id': self.id,
            'user_id': User.query.filter(User.id == self.user_id).first().name,
            'devid': self.devid,
            'brand': self.brand,
            # 'add_for': User.query.filter(User.id == self.add_for).first().name,
            'model': self.model,
            'registry': self.registry,
            'general_description': self.general_description,
            'type': self.type
        }

    def __repr__(self):
        return str(self.id)

    def is_admin(self):
        admin = Admin.query.filter(Admin.user_id == self.user_id).first()
        if admin is not None:
            return True
        else:
            return False

    __table_args__ = (
        db.UniqueConstraint(
            id, user_id),
    )


class EquipmentUsageHistory(db.Model):
    __tablename__ = "equipment_usage_histories"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    equip_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_receive = db.Column(db.String(64), nullable=False)
    date_return = db.Column(db.String(64), nullable=True)
    observation = db.Column(db.String(700), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'equip_id': self.equip_id,
            'date_receive': self.date_receive,
            'date_return': self.date_return,
            'observation': self.observation,
            'user_id': User.query.filter(User.id == self.user_id).first().name,
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    leader = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Nome %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    # register = db.Column(db.String(64), nullable=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False, default="Dia 2 de fevereiro é o dia mais lindo que há")
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    all_equipments = db.relationship("EquipmentUsageHistory", backref="equipment_usage_histories",
                                     foreign_keys='EquipmentUsageHistory.user_id')

    # __table_args__ = (
    #     db.UniqueConstraint(
    #         register, name),
    # )

    def is_admin(self):
        admin = Admin.query.filter(Admin.admin_id == self.id).first()
        if admin is not None:
            return True
        else:
            return False

    @property
    def set_password(self):
        raise AttributeError('não é permitido ler a senha')

    def verify_password(self, password):
        if self.password == password and self.password is not None:
            return True
        return False

    def get_id(self):
        return self.id

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_dict(self):

        return {
            'id': self.id,
            # 'register': self.register,
            'name': self.name,
            'team_id': Team.query.filter(Team.id == self.team_id).first().name,

        }

    def __repr__(self):
        return self.name


class Admin(User):
    __tablename__ = 'admins'
    # admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    admin_name = db.Column(db.String(64), unique=True)

    # admin_pass_wd = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.admin_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@event.listens_for(Team.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Team(id=1, name="Smart Coffe", leader="Alexandre MaeSato"))
    db.session.add(Team(id=2, name="Linkin Dart", leader="Rodrigo"))
    db.session.add(Team(id=3, name="QA", leader="Diana Souza"))
    db.session.add(Team(id=4, name="Produto", leader="Produto"))
    db.session.add(Team(id=5, name="Genérico", leader="Genérico"))
    db.session.add(Team(id=6, name="PO", leader="Valeria Villaverde"))
    db.session.add(Team(id=7, name="SM", leader="Uriel Boscolo"))
    db.session.commit()


@event.listens_for(User.__table__, 'after_create')
def insert_initial_values3(*ars, **kwargs):
    db.session.add(User(
        name="Alexandre Maesato", team_id=1))
    db.session.add(User(
        name="Uriel Boscolo", team_id=7))
    db.session.add(User(
        name="Rodrigo Knop", team_id=1))
    db.session.add(User(
        name="Jean Will", team_id=1))
    db.session.add(User(
        name="Altieres ", team_id=1))
    db.session.add(User(
        name="Douglas Novaki", team_id=1))
    db.session.add(User(
        name="Kleyton Lucas de Souza", team_id=1))
    db.session.add(User(
        name="Igor Alfredo Fortti", team_id=1))
    db.session.add(User(name="Andrew Oliveira", team_id=1))
    db.session.add(User(name="Diana Souza", team_id=3))
    db.session.add(User(name="Sarah Silva", team_id=3))
    db.session.add(User(
        name="Alessandra Silva", team_id=3))
    db.session.add(User(name="Nelson Gonzales", team_id=3))
    db.session.add(User(name="Valeria VillaVerde", team_id=6))
    db.session.commit()
