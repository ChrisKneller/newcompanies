"""Temporarily changed User sub types

Revision ID: f54d39418e2d
Revises: d6425195a676
Create Date: 2020-05-18 09:08:25.131994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f54d39418e2d'
down_revision = 'd6425195a676'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sub_type', sa.Integer(), nullable=True))
    op.drop_column('users', 'subscription_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('subscription_type', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('users', 'sub_type')
    # ### end Alembic commands ###