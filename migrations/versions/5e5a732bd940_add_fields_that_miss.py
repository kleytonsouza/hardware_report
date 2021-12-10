"""add fields that miss

Revision ID: 5e5a732bd940
Revises: 043b142a3fa2
Create Date: 2021-11-16 10:44:10.154446

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5e5a732bd940'
down_revision = '043b142a3fa2'
branch_labels = None
depends_on = None


def upgrade():
    pass
        ## commands auto generated by Alembic - please adjust! ###
        # op.create_table('storages',
        # sa.Column('storage_id', sa.Integer(), nullable=False),
        # sa.Column('storage_name', sa.String(length=64), nullable=True),
        # sa.Column('storage_size', sa.String(length=64), nullable=False),
        # sa.Column('storage_type', sa.String(length=64), nullable=True),
        # sa.Column('storage_computer', sa.Integer(), nullable=True),
        # sa.ForeignKeyConstraint(['storage_computer'], ['computers.computer_id'], ),
        # sa.ForeignKeyConstraint(['storage_id'], ['equipments.equip_id'], ),
        # sa.PrimaryKeyConstraint('storage_id')
        # )
        # op.alter_column('calls', 'call_user_id',
        #            existing_type=mysql.INTEGER(),
        #            nullable=False)
        # op.drop_index('call_user_id_idx', table_name='calls')
        # op.add_column('computers', sa.Column('computer_name', sa.String(length=64), nullable=False))
        # op.add_column('computers', sa.Column('computer_so', sa.String(length=64), nullable=True))
        # op.add_column('computers', sa.Column('computer_bios', sa.String(length=64), nullable=True))
        # op.add_column('computers', sa.Column('computer_macaddress', sa.String(length=64), nullable=True))
        # op.add_column('computers', sa.Column('computer_capacity_memory', sa.String(length=64), nullable=True))
        # op.create_unique_constraint(None, 'computers', ['computer_name'])
        # op.add_column('equipments', sa.Column('position', sa.String(length=64), nullable=True))
     ### end Alembic commands ###


    # def downgrade():
    #     # ### commands auto generated by Alembic - please adjust! ###
    #     op.drop_column('equipments', 'position')
    #     op.drop_constraint(None, 'computers', type_='unique')
    #     op.drop_column('computers', 'computer_capacity_memory')
    #     op.drop_column('computers', 'computer_macaddress')
    #     op.drop_column('computers', 'computer_bios')
    #     op.drop_column('computers', 'computer_so')
    #     op.drop_column('computers', 'computer_name')
    #     op.create_index('call_user_id_idx', 'calls', ['call_user_id'], unique=False)
    #     op.alter_column('calls', 'call_user_id',
    #                existing_type=mysql.INTEGER(),
    #                nullable=True)
    #     op.drop_table('storages')
        # ### end Alembic commands ###
