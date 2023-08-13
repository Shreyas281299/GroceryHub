"""empty message

Revision ID: 5cd9877d7cd8
Revises: 07824ca53de8
Create Date: 2023-08-08 01:32:46.092686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cd9877d7cd8'
down_revision = '07824ca53de8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('addedOnDate', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_model', schema=None) as batch_op:
        batch_op.drop_column('addedOnDate')

    # ### end Alembic commands ###