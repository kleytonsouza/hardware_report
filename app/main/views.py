from . import main
from flask import redirect, url_for

from ..models import User


@main.route('/')
def index():
    return redirect(url_for('auth.login'))



@main.route('/giramundo')
def giramundo():
    return "<h1>Giramundo</h1>"


@main.route('/api/usuarios')
def listar_usuarios():
    users = User.query.all()

    # return f"""
    #     <h1>Lista de Usuarios</h1>
    #     <table>
    #     <tr>{user}</tr>
    #     </table>
    #     """
    # Gerar linhas da tabela
    table_rows = "".join(f"<tr><td>{user.name}</td><td>{user.team_id}</td></tr>" for user in users)

    # HTML completo
    html_content = f"""
    <h1>Lista de Usuários</h1>
    <table>
        <tr><th>Nome</th><th>Team ID</th></tr>
        {table_rows}
    </table>
    """

    return html_content