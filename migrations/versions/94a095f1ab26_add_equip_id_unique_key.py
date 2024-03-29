"""add equip_id unique key

Revision ID: 94a095f1ab26
Revises: 0f8bba5e35ab
Create Date: 2021-12-15 15:04:33.912555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94a095f1ab26'
down_revision = '0f8bba5e35ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('patrimony', table_name='equipments')
    op.create_unique_constraint(None, 'equipments', ['patrimony', 'equip_user_id', 'equip_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'equipments', type_='unique')
    op.create_index('patrimony', 'equipments', ['patrimony', 'equip_user_id'], unique=False)
    # ### end Alembic commands ###
