from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    user = StringField('User', validators=[DataRequired()], render_kw={"placeholder": "Admin User"})
    password = PasswordField('PassWord', validators=[DataRequired()],
                             render_kw={"placeholder": "Admin Pass"})
    # remember_me = BooleanField('Mantenha-me Logado')
    submit = SubmitField('Go')