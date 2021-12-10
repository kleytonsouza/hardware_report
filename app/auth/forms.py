from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, SelectField
from wtforms.validators import DataRequired
from ..models import *


class LoginForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()],
                       render_kw={"placeholder": "Admin User", "autocomplete": "on"})
    password = PasswordField('PassWord', validators=[DataRequired()],
                             render_kw={"placeholder": "Admin Pass", "autocomplete": "on"})
    submit = SubmitField('Go')


def form_add_type_equip():
    class AddTypeEquip(FlaskForm):
        submit = SubmitField('Registrar')

    setattr(AddTypeEquip, 'type', RadioField("", validators=[DataRequired()]))

    return AddTypeEquip()


def form_add_equip():

    class AddEquipForm(FlaskForm):
        choices = [(s.user_id, s.user_name) for s in User.query.distinct(User.user_name).all()]
        choices.append((" ", "Selecione o Usuário"))

        equip_user = SelectField('Usuário',
                                 choices=choices, default=" ",
                                 validators=[DataRequired()])
        patrimony = IntegerField('Patrimonio',
                                 render_kw={"placeholder": "Digite o Patrimonio", "autocomplete": "on"})
        brand = StringField('Marca',
                            render_kw={"placeholder": "Digite a Marca", "autocomplete": "on"})
        model = StringField('Modelo',
                            render_kw={"placeholder": "Digite o modelo", "autocomplete": "on"})
        position = StringField('Posição',
                               render_kw={"placeholder": "Posição do computador", "autocomplete": "on"})
        general_description = StringField('Descrição Geral', validators=[DataRequired()],
                                          render_kw={"placeholder": "Descreva caracteristicas", "autocomplete": "on"})
        submit = SubmitField("Registrar")

    return AddEquipForm


def form_add_computer():

    class AddComputerForm(form_add_equip()):
        # computer_id =
        computer_name = StringField('Nome do Computador',
                                    render_kw={"placeholder": "Digite o nome do computador", "autocomplete": "on"})
        computer_so = StringField('Sistema Operacional',
                                  render_kw={"placeholder": "Digite o Sistema Operacional", "autocomplete": "on"})
        computer_bios = StringField('BIOS',
                                    render_kw={"placeholder": "Digite o modelo e versão da BIOS", "autocomplete": "on"})
        computer_cpu = StringField('Processador',
                                      render_kw={"placeholder": "Digite o modelo do Processador", "autocomplete": "on"})
        computer_memory = StringField('Memória',
                                      render_kw={"placeholder": "Digita a quantidade de memória RAM", "autocomplete": "on"})
        computer_hd = StringField('Hard Disc',
                                      render_kw={"placeholder": "Digite o Tamanho do Armazenamento", "autocomplete": "on"})
        computer_vga = StringField('Placa de Vídeo',
                                   render_kw={"placeholder": "Digite o modelo da placa de vídeo", "autocomplete": "on"})
        computer_macaddress = StringField('Mac Address',
                                          render_kw={"placeholder": "Digite o Mac Address", "autocomplete": "on"})
        computer_capacity_memory = StringField('Capacidade de Memória', validators=[DataRequired()],
                                               render_kw={"placeholder": "Digite a capacidade de Memória",
                                                          "autocomplete": "on"})

    return AddComputerForm()
