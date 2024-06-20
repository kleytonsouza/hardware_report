from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length

from ..models import *


class LoginForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()],
                       render_kw={"placeholder": "Admin User", "autocomplete": "on"})
    password = PasswordField('PassWord', validators=[DataRequired()],
                             render_kw={"placeholder": "Admin Pass", "autocomplete": "on"})
    submit = SubmitField('Go')


#
# def form_add_type_equip():
#     class AddTypeEquip(FlaskForm):
#         submit = SubmitField('Registrar')
#
#     setattr(AddTypeEquip, 'type', RadioField("", validators=[DataRequired()]))
#
#     return AddTypeEquip()


def form_add_user():
    class AddUserForm(FlaskForm):
        coords = []
        for i in Team.query.all():
            coords.append((i.id, i.name))

        choices = coords
        choices.append((" ", "Selecione o Time"))
        # choices_sub = [(t.team_id, t.team_name) for t in SubTeam.query.distinct(SubTeam.subteam_id).all()]
        # choices_sub.append((" ", "Selecione a Subcoordenação"))
        register = IntegerField('Registro Funcional',
                                render_kw={"placeholder": "Digite o Registro funcional", "autocomplete": "on"})
        name = StringField('Nome do Usuário',
                           render_kw={"placeholder": "Digite o modelo", "autocomplete": "on"})
        team_id = SelectField('Time',
                              choices=choices, default=" ",
                              validators=[DataRequired()])
        # User_subteam_id = SelectField('Subcoordenação',
        #                               choices=choices_sub, default=" ",
        #                               validators=[DataRequired()])

    return AddUserForm()


def form_edit_user(user):
    class EditUserForm(FlaskForm):
        coords = []
        for i in Team.query.all():
            coords.append((i.id, i.name))

        choices = coords
        choices.append((" ", "Selecione o Time"))
        name = StringField('Nome do Usuário', default=user.name,
                           render_kw={"placeholder": "Digite o nome", "autocomplete": "on"})
        team_id = SelectField('Time', default=user.team_id,
                              choices=choices,
                              validators=[DataRequired()])
        submit = SubmitField("Registrar")

    return EditUserForm


def form_add_equip():
    class AddEquipForm(FlaskForm):
        choices = [(s.id, s.name) for s in User.query.distinct(User.name).all()]
        # choices.append((" ", "Selecione o Usuário"))
        equip_user = SelectField('Usuário', choices=choices, validators=[DataRequired()])
        devid = StringField('Dev ID',
                            render_kw={"placeholder": "Digite o DevId", "autocomplete": "on"},
                            validators=[DataRequired()])
        brand = StringField('Marca',
                            render_kw={"placeholder": "Digite a Marca", "autocomplete": "on"},
                            validators=[DataRequired()])
        add_for = current_user.id
        model = StringField('Modelo',
                            render_kw={"placeholder": "Digite o modelo", "autocomplete": "on"},
                            validators=[DataRequired()])
        type = StringField('Tipo',
                           render_kw={"placeholder": "O Tipo do Equipamento", "autocomplete": "on"},
                           validators=[DataRequired()])
        general_description = StringField('Descrição Geral',
                                          render_kw={"placeholder": "Anotações pertinentes", "autocomplete": "on"})
        submit = SubmitField("Registrar")

    return AddEquipForm


def form_edit_equip(equip):
    class EditEquipForm(FlaskForm):
        choices = [(s.id, s.name) for s in User.query.distinct(User.name).all()]
        # choices.append((" ", "Selecione o Usuário"))
        equip_user = SelectField('Usuário',
                                 choices=choices, default=equip.user_id,
                                 validators=[DataRequired()])
        brand = StringField('Marca', default=equip.brand,
                            render_kw={"placeholder": "Digite a Marca", "autocomplete": "on"})
        devid = StringField('DevId', default=equip.devid,
                            render_kw={"placeholder": "Digite o DevI", "autocomplete": "on"})
        model = StringField('Modelo', default=equip.model,
                            render_kw={"placeholder": "Digite o modelo", "autocomplete": "on"})
        type = StringField('Tipo', default=equip.type,
                           render_kw={"placeholder": "Tipo do Equipamento", "autocomplete": "on"})
        general_description = StringField('Descrição Geral', validators=[DataRequired()],
                                          default=equip.general_description,
                                          render_kw={"placeholder": "Descreva caracteristicas", "autocomplete": "on"})
        submit = SubmitField("Registrar")

    return EditEquipForm


def form_close_history():
    class AddEquipForm(FlaskForm):
        choices = [(s.user_id, s.user_name) for s in User.query.distinct(User.user_name).all()]
        # choices.append((" ", "Selecione o Usuário"))
        equip_user = SelectField('Usuário',
                                 choices=choices,  # default=35,
                                 validators=[DataRequired()])
        devid = StringField('DevId',
                            render_kw={"placeholder": "Digite o DevId", "autocomplete": "on"})
        brand = StringField('Marca',
                            render_kw={"placeholder": "Digite a Marca", "autocomplete": "on"})
        model = StringField('Modelo',
                            render_kw={"placeholder": "Digite o modelo", "autocomplete": "on"})
        equip_type = StringField('Tipo',
                                 render_kw={"placeholder": "O Equipamento é um?", "autocomplete": "on"})
        general_description = StringField('Descrição Geral', validators=[DataRequired()],
                                          render_kw={"placeholder": "Descreva caracteristicas", "autocomplete": "on"})
        submit = SubmitField("Registrar")

    return AddEquipForm


def form_open_history():
    class OpenHistoryForm(FlaskForm):
        user_id = SelectField('Identificação do Usuário', choices=User.query.all(),
                              render_kw={"placeholder": "Digite o usuário", "autocomplete": "on"})

        equip_id = SelectField('Identificação do Equipamento', choices=Equipment.query.all(),
                               render_kw={"placeholder": "Digite o modelo", "autocomplete": "on"})
        # call_technician = SelectField('Coordenação', choices=Admin.query.all())
        date_receive = DateField('Data do Recebimento', render_kw={"placeholder": "Selecione a data de recebimento"},
                                 format="%d-%m-%Y",
                                 validators=[DataRequired(message="A Data de Recebimento é obrigatória.")])
        date_return = DateField('Data da Entrega', render_kw={"placeholder": "Selecione a data de entrega"},
                                format="%d-%m-%Y", validators=[])
        observation = TextAreaField('Observação',
                                    render_kw={"placeholder": "Descreva uma observação (10 a 370 caracs.)",
                                               "autocomplete": "on"},
                                    validators=[Length(min=0, max=370, message="Min 10 e max 370")])

    return OpenHistoryForm()

#
# def form_edit_computer(equip):
#     edit_equip_form = form_edit_equip(equip)
#
#     class EditComputerForm(edit_equip_form):
#         computer = Computer.query.filter(Computer.computer_id == equip.equip_id).first()
#         computer_name = StringField('Nome do Computador', default=computer.computer_name,
#                                     render_kw={"placeholder": "Digite o nome do computador", "autocomplete": "on"})
#         computer_so = StringField('Sistema Operacional', default=computer.computer_so,
#                                   render_kw={"placeholder": "Digite o Sistema Operacional", "autocomplete": "on"})
#         computer_bios = StringField('BIOS', default=computer.computer_bios,
#                                     render_kw={"placeholder": "Digite o modelo e versão da BIOS", "autocomplete": "on"})
#         computer_cpu = StringField('Processador', default=computer.computer_cpu,
#                                    render_kw={"placeholder": "Digite o modelo do Processador", "autocomplete": "on"})
#         computer_memory = StringField('Memória', default=computer.computer_memory,
#                                       render_kw={"placeholder": "Digita a quantidade de memória RAM",
#                                                  "autocomplete": "on"})
#         computer_hd = StringField('Hard Disc', default=computer.computer_hd,
#                                   render_kw={"placeholder": "Digite o Tamanho do Armazenamento", "autocomplete": "on"})
#         computer_vga = StringField('Placa de Vídeo', default=computer.computer_vga,
#                                    render_kw={"placeholder": "Digite o modelo da placa de vídeo", "autocomplete": "on"})
#         computer_macaddress = StringField('Mac Address', default=computer.computer_macaddress,
#                                           render_kw={"placeholder": "Digite o Mac Address", "autocomplete": "on"})
#         computer_capacity_memory = StringField('Capacidade de Memória', default=computer.computer_capacity_memory,
#                                                render_kw={"placeholder": "Digite a capacidade de Memória",
#                                                           "autocomplete": "on"})
#         computer_storages = StringField('Capacidade de Memória', default=computer.computer_capacity_memory,
#                                         render_kw={"placeholder": "Digite a capacidade de Memória",
#                                                    "autocomplete": "on"})
#
#     return EditComputerForm()
#
#
# def form_add_computer():
#     class AddComputerForm(form_add_equip()):
#         computer_name = StringField('Nome do Computador',
#                                     render_kw={"placeholder": "Digite o nome do computador", "autocomplete": "on"})
#         computer_so = StringField('Sistema Operacional',
#                                   render_kw={"placeholder": "Digite o Sistema Operacional", "autocomplete": "on"})
#         computer_bios = StringField('BIOS',
#                                     render_kw={"placeholder": "Digite o modelo e versão da BIOS", "autocomplete": "on"})
#         computer_cpu = StringField('Processador',
#                                    render_kw={"placeholder": "Digite o modelo do Processador", "autocomplete": "on"})
#         computer_memory = StringField('Memória',
#                                       render_kw={"placeholder": "Digita a quantidade de memória RAM",
#                                                  "autocomplete": "on"})
#         computer_hd = StringField('Hard Disc',
#                                   render_kw={"placeholder": "Digite o Tamanho do Armazenamento", "autocomplete": "on"})
#         computer_vga = StringField('Placa de Vídeo',
#                                    render_kw={"placeholder": "Digite o modelo da placa de vídeo", "autocomplete": "on"})
#         computer_macaddress = StringField('Mac Address',
#                                           render_kw={"placeholder": "Digite o Mac Address", "autocomplete": "on"})
#         computer_capacity_memory = StringField('Capacidade de Memória',
#                                                render_kw={"placeholder": "Digite a capacidade de Memória",
#                                                           "autocomplete": "on"})
#
#     return AddComputerForm()
#
#
# def form_edit_monitor(equip):
#     edit_equip_form = form_edit_equip(equip)
#
#     class EditMonitorForm(edit_equip_form):
#         monitor = Monitor.query.filter(Monitor.monitor_id == equip.equip_id).first()
#         monitor_size = StringField('Tamanho do Monitor', default=monitor.monitor_size,
#                                    render_kw={"placeholder": "Digite o tamanho em polegas do monitor",
#                                               "autocomplete": "on"})
#         monitor_resolution = StringField('Resolução do Monitor', default=monitor.monitor_resolution,
#                                          render_kw={"placeholder": "Digite a resolução da tela", "autocomplete": "on"})
#
#     return EditMonitorForm()
#
#
# def form_add_monitor():
#     class AddMonitorForm(form_add_equip()):
#         # computer_id =
#         monitor_size = StringField('Tamanho do Monitor',
#                                    render_kw={"placeholder": "Digite o tamanho em polegas do monitor",
#                                               "autocomplete": "on"})
#         monitor_resolution = StringField('Resolução do Monitor',
#                                          render_kw={"placeholder": "Digite a resolução da tela", "autocomplete": "on"})
#
#     return AddMonitorForm()
#
#
# def form_add_webcam():
#     class AddWebcamForm(form_add_equip()):
#         # computer_id =
#         webcam_resolution = StringField('Resolução da Webcam',
#                                         render_kw={"placeholder": "Digite a resolução da webcam", "autocomplete": "on"})
#
#     return AddWebcamForm()
#
#
# def form_edit_webcam(equip):
#     edit_equip_form = form_edit_equip(equip)
#
#     class EditWebcamForm(edit_equip_form):
#         webcam = WebCam.query.filter(WebCam.webcam_id == equip.equip_id).first()
#         webcam_resolution = StringField('Resolução da Webcam', default=webcam.webcam_resolution,
#                                         render_kw={"placeholder": "Digite a resolução da webcam", "autocomplete": "on"})
#
#     return EditWebcamForm()
#
#
# def form_add_fone():
#     class AddFoneForm(form_add_equip()):
#         choices = [(m.mic_id, m.model) for m in Mic.query.distinct(Mic.model).all()]
#         choices.append((" ", "Selecione o Microfone"))
#
#         fone_frequency = StringField('Frequência do Fone',
#                                      render_kw={"placeholder": "Digite o nome a frequência do fone",
#                                                 "autocomplete": "on"})
#
#         fone_impedance = StringField('Impedância do Fone',
#                                      render_kw={"placeholder": "Digite a impedância do fone", "autocomplete": "on"})
#
#         fone_driver = StringField('Driver do Fone',
#                                   render_kw={"placeholder": "Digite o driver do fone", "autocomplete": "on"})
#
#         fone_noise_cancellation = StringField('Cancelamento de Ruído',
#                                               render_kw={"placeholder": "Digite se possui cancelamento de ruído",
#                                                          "autocomplete": "on"})
#
#     return AddFoneForm()
#
#
# def form_edit_fone(equip):
#     edit_equip_form = form_edit_equip(equip)
#
#     class EditFoneForm(edit_equip_form):
#         fone = Fone.query.filter(Fone.fone_id == equip.equip_id).first()
#         choices = [(m.mic_id, m.model) for m in Mic.query.distinct(Mic.model).all()]
#         choices.append((" ", "Selecione o Microfone"))
#
#         fone_frequency = StringField('Frequência do Fone', default=fone.fone_frequency,
#                                      render_kw={"placeholder": "Digite o nome a frequência do fone",
#                                                 "autocomplete": "on"})
#
#         fone_impedance = StringField('Impedância do Fone', default=fone.fone_impedance,
#                                      render_kw={"placeholder": "Digite a impedância do fone", "autocomplete": "on"})
#
#         fone_driver = StringField('Driver do Fone', default=fone.fone_driver,
#                                   render_kw={"placeholder": "Digite o driver do fone", "autocomplete": "on"})
#
#         fone_noise_cancellation = StringField('Cancelamento de Ruído', default=fone.fone_noise_cancellation,
#                                               render_kw={"placeholder": "Digite se possui cancelamento de ruído",
#                                                          "autocomplete": "on"})
#
#     return EditFoneForm()
#
#
# def form_add_mic():
#     class AddMicForm(form_add_equip()):
#         mic_frequency = StringField('Frequência do Microfone',
#                                     render_kw={"placeholder": "Digite a Frequência do fone", "autocomplete": "on"})
#
#         mic_impedance = StringField('Impedância do Microfone',
#                                     render_kw={"placeholder": "Digite a impedância do fone", "autocomplete": "on"})
#
#         mic_noise_cancellation = StringField('R',
#                                              render_kw={"placeholder": "Digite se possui cancelamento de ruído",
#                                                         "autocomplete": "on"})
#
#     return AddMicForm()
#
#
# def form_edit_mic(equip):
#     edit_equip_form = form_edit_equip(equip)
#
#     class EditMicForm(edit_equip_form):
#         mic = Mic.query.filter(Mic.mic_id == equip.equip_id).first()
#         mic_frequency = StringField('Frequência do microfone', default=mic.mic_frequency,
#                                     render_kw={"placeholder": "Digite a Frequência do fone", "autocomplete": "on"})
#
#         mic_impedance = StringField('Impedância do microfone', default=mic.mic_impedance,
#                                     render_kw={"placeholder": "Digite a impedância do fone", "autocomplete": "on"})
#
#         mic_noise_cancellation = StringField('Cancelamento de ruído', default=mic.mic_noise_cancellation,
#                                              render_kw={"placeholder": "Digite se possui cancelamento de ruído",
#                                                         "autocomplete": "on"})
#
#     return EditMicForm()
