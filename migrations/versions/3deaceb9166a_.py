"""empty message

Revision ID: 3deaceb9166a
Revises: 07e8f72e2c58
Create Date: 2023-08-09 00:44:45.447845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3deaceb9166a'
down_revision = '07e8f72e2c58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('popularity', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_model', schema=None) as batch_op:
        batch_op.drop_column('popularity')

    # ### end Alembic commands ###
