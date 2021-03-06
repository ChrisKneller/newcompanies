"""Added user model

Revision ID: 95e3c60ba70d
Revises: aa13cc2bbbe3
Create Date: 2020-05-17 10:01:42.030065

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

SUB_TYPES = [
    (0, "Free"),
    (1, "Standard"),
    (2, "Advanced"),
    (3, "Enterprise"),
]

# revision identifiers, used by Alembic.
revision = '95e3c60ba70d'
down_revision = 'aa13cc2bbbe3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('record_created', sa.DateTime(), nullable=True),
    sa.Column('record_updated', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('subscription_type', sqlalchemy_utils.types.choice.ChoiceType(SUB_TYPES), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('addresses', sa.Column('record_updated', sa.DateTime(), nullable=True))
    op.add_column('companies', sa.Column('record_updated', sa.DateTime(), nullable=True))
    op.add_column('siccodes', sa.Column('record_updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('siccodes', 'record_updated')
    op.drop_column('companies', 'record_updated')
    op.drop_column('addresses', 'record_updated')
    op.drop_table('users')
    # ### end Alembic commands ###
