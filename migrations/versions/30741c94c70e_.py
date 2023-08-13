"""empty message

Revision ID: 30741c94c70e
Revises: f7c2b06d62c3
Create Date: 2023-08-13 16:00:17.943143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30741c94c70e'
down_revision = 'f7c2b06d62c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_order')
    with op.batch_alter_table('user_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstOrder', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_model', schema=None) as batch_op:
        batch_op.drop_column('firstOrder')

    op.create_table('user_order',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('userId', sa.INTEGER(), nullable=True),
    sa.Column('orderHistory', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['user_model.uuid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
