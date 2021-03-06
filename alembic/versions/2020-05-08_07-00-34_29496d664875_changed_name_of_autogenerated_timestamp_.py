"""Changed name of autogenerated timestamp field

Revision ID: 29496d664875
Revises: f5a5383d57f5
Create Date: 2020-05-08 07:00:34.630867

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '29496d664875'
down_revision = 'f5a5383d57f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('record_created', sa.DateTime(), nullable=True))
    # op.add_column('companies', sa.Column('record_created', sa.DateTime(), nullable=True))
    # op.drop_column('companies', 'created')
    # op.alter_column('addresses', 'created', new_column_name='record_created')
    op.alter_column('companies', 'created', new_column_name='record_created')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('companies', sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # op.drop_column('companies', 'record_created')
    op.drop_column('addresses', 'record_created')
    # op.alter_column('addresses', 'created', new_column_name='record_created')
    op.alter_column('companies', 'record_created', new_column_name='created')
    # ### end Alembic commands ###
