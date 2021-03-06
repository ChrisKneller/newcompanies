"""changed col name

Revision ID: 7dae4ff5cf0e
Revises: 5fa3444f5d2c
Create Date: 2020-05-07 12:26:57.189924

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7dae4ff5cf0e'
down_revision = '5fa3444f5d2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('createdAt', sa.DateTime(), nullable=True))
    op.drop_column('companies', 'created_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('companies', 'createdAt')
    # ### end Alembic commands ###
