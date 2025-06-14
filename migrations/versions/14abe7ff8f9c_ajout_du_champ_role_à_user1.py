"""Ajout du champ role à user1

Revision ID: 14abe7ff8f9c
Revises: 
Create Date: 2025-06-10 18:41:45.533134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14abe7ff8f9c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user1', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
