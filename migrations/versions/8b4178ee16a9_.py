"""empty message

Revision ID: 8b4178ee16a9
Revises: 84093645e32e
Create Date: 2023-07-11 02:38:16.079085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b4178ee16a9'
down_revision = '84093645e32e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ticketRequest', sa.String(), nullable=False))
        batch_op.drop_column('ticektRequest')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ticektRequest', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('ticketRequest')

    # ### end Alembic commands ###