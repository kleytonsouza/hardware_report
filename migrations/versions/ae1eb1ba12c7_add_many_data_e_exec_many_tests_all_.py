"""add many data e exec many tests all right ok

Revision ID: ae1eb1ba12c7
Revises: 4b2b7ee66927
Create Date: 2021-11-09 21:20:25.513696

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ae1eb1ba12c7'
down_revision = '4b2b7ee66927'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('equipments', sa.Column('equip_registry', sa.String(length=64), nullable=True))
    op.drop_column('equipments', 'registry')
    op.add_column('subteams', sa.Column('subteam_name', sa.String(length=64), nullable=False))
    op.drop_column('subteams', 'subtime_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subteams', sa.Column('subtime_name', mysql.VARCHAR(length=64), nullable=False))
    op.drop_column('subteams', 'subteam_name')
    op.add_column('equipments', sa.Column('registry', mysql.VARCHAR(length=64), nullable=True))
    op.drop_column('equipments', 'equip_registry')
    # ### end Alembic commands ###
