import os

import click
from flask_migrate import Migrate

from app import create_app
from app.models import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Equipment=Equipment,
                Computer=Computer, Monitor=Monitor,
                Fone=Fone, Mic=Mic, Call=Call,
                WebCam=WebCam, Connection=Connection,
                User=User, Admin=Admin, EquipmentConnection=EquipmentConnection,
                Team=Team, SubTeam=SubTeam)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
