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


def form_add_user():
    class AddUserForm(FlaskForm):
        coords = []
        for i in Team.query.all():
            if SubTeam.query.filter(SubTeam.subteam_team_id == i.team_id).first() is not None:
                for c in SubTeam.query.filter(SubTeam.subteam_team_id == i.team_id).all():
                    coords.append(([i.team_id, c.subteam_id], i.team_name + " - " + c.subteam_name))
            else:
                coords.append((i.team_id, i.team_name))

        choices = coords
        choices.append((" ", "Selecione a Coordenação"))

        # choices_sub = [(t.team_id, t.team_name) for t in SubTeam.query.distinct(SubTeam.subteam_id).all()]
        # choices_sub.append((" ", "Selecione a Subcoordenação"))

        user_register = IntegerField('Registro Funcional',
                                     render_kw={"placeholder": "Digite o Patrimonio", "autocomplete": "on"})
        user_name = StringField('Nome do Usuário',
                                render_kw={"placeholder": "Digite o modelo", "autocomplete": "on"})
        user_team_id = SelectField('Coordenação',
                                   choices=choices, default=" ",
                                   validators=[DataRequired()])
        # User_subteam_id = SelectField('Subcoordenação',
        #                               choices=choices_sub, default=" ",
        #                               validators=[DataRequired()])

    return AddUserForm()


def form_add_equip():
    class AddEquipForm(FlaskForm):
        choices = [(s.user_id, s.user_name) for s in User.query.distinct(User.user_name).all()]
        choices.append((" ", "Selecione o Usuário"))

        equip_user = SelectField('Usuário',
                                 choices=choices, default=" ",
                                 validators=[DataRequired()])
        patrimony = StringField('Patrimonio',
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

        computer_name = StringField('Nome do Computador',
                                    render_kw={"placeholder": "Digite o nome do computador", "autocomplete": "on"})
        computer_so = StringField('Sistema Operacional',
                                  render_kw={"placeholder": "Digite o Sistema Operacional", "autocomplete": "on"})
        computer_bios = StringField('BIOS',
                                    render_kw={"placeholder": "Digite o modelo e versão da BIOS", "autocomplete": "on"})
        computer_cpu = StringField('Processador',
                                   render_kw={"placeholder": "Digite o modelo do Processador", "autocomplete": "on"})
        computer_memory = StringField('Memória',
                                      render_kw={"placeholder": "Digita a quantidade de memória RAM",
                                                 "autocomplete": "on"})
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


def form_add_monitor():
    class AddMonitorForm(form_add_equip()):
        # computer_id =
        monitor_size = StringField('Tamanho do Monitor',
                                   render_kw={"placeholder": "Digite o tamanho em polegas do monitor",
                                              "autocomplete": "on"})
        monitor_resolution = StringField('Resolução do Monitor',
                                         render_kw={"placeholder": "Digite a resolução da tela", "autocomplete": "on"})

    return AddMonitorForm()


def form_add_webcam():
    class AddWebcamForm(form_add_equip()):
        # computer_id =
        webcam_resolution = StringField('Resolução da Webcam',
                                        render_kw={"placeholder": "Digite a resolução da webcam", "autocomplete": "on"})

    return AddWebcamForm()


def form_add_fone():
    class AddFoneForm(form_add_equip()):
        choices = [(m.mic_id, m.model) for m in Mic.query.distinct(Mic.model).all()]
        choices.append((" ", "Selecione o Microfone"))

        fone_frequency = StringField('Frequência do Fone',
                                     render_kw={"placeholder": "Digite o nome a frequência do fone",
                                                "autocomplete": "on"})

        fone_impedance = StringField('Impedância do Fone',
                                     render_kw={"placeholder": "Digite a impedância do fone", "autocomplete": "on"})

        fone_driver = StringField('Driver do Fone',
                                  render_kw={"placeholder": "Digite o driver do fone", "autocomplete": "on"})

        fone_noise_cancellation = StringField('Cancelamento de Ruído',
                                              render_kw={"placeholder": "Digite se possui cancelamento de ruído",
                                                         "autocomplete": "on"})

    return AddFoneForm()


def form_add_mic():
    class AddMicForm(form_add_equip()):
        mic_frequency = StringField('Frequência do microfone',
                                    render_kw={"placeholder": "Digite a Frequência do fone", "autocomplete": "on"})

        mic_impedance = StringField('Impedância do microfone',
                                    render_kw={"placeholder": "Digite a impedância do fone", "autocomplete": "on"})

        mic_noise_cancellation = StringField('Cancelamento de ruído',
                                             render_kw={"placeholder": "Digite se possui cancelamento de ruído",
                                                        "autocomplete": "on"})

    return AddMicForm()
