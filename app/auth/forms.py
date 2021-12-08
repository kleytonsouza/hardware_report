from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from ..models import *


class LoginForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()], render_kw={"placeholder": "Admin User", "autocomplete": "on"})
    password = PasswordField('PassWord', validators=[DataRequired()],
                             render_kw={"placeholder": "Admin Pass", "autocomplete": "on"})
    submit = SubmitField('Go')


def form_add_type_equip():

    class AddTypeEquip(FlaskForm):
        submit = SubmitField('Registrar')

    setattr(AddTypeEquip,  'type', RadioField("", validators=[DataRequired()]))

    return AddTypeEquip()


def form_add_equip():

    class AddEquipForm(FlaskForm):
        submit = SubmitField("Registrar")

    setattr(AddEquipForm, "fields", TextAreaField(""))

    return "jiboia"
    # return AddEquipForm

    # for name_class in Equipment.__subclasses__():
    #     if name_class.__name__ == type:
    #         return

    # patrimony = IntegerField('Patrimonio',
    #                    render_kw={"placeholder": "Digite o Patrimonio", "autocomplete": "on"})
    # brand = StringField('Marca',
    #                    render_kw={"placeholder": "Digite a Marca", "autocomplete": "on"})
    # model = StringField('Modelo',
    #                    render_kw={"placeholder": "Digite o modele", "autocomplete": "on"})
    # position = StringField('Posição',
    #                    render_kw={"placeholder": "Posição do computador", "autocomplete": "on"})
    # # pegar a data do sumit do form.
    # #equip_registry = StringField('User', validators=[DataRequired()],
    # #                    render_kw={"placeholder": "Admin User", "autocomplete": "on"})
    # general_description = StringField('Descrição Geral', validators=[DataRequired()],
    #                    render_kw={"placeholder": "Descreva caracteristicas", "autocomplete": "on"})
    # type = RadioField('Selecione o tipo', validators=[DataRequired()],
    #                        render_kw={"placeholder": "Qual o tipo do equipamento", "autocomplete": "on"})


