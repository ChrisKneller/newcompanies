"""Your message

Revision ID: 6be013d6fdb9
Revises: 6b2240ac64a1
Create Date: 2020-05-07 11:31:10.926625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6be013d6fdb9'
down_revision = '6b2240ac64a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('companies', 'incorporated_on', nullable=False, new_column_name='incorporated')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('companies', 'incorporated', nullable=False, new_column_name='incorporated_on')
    # ### end Alembic commands ###
