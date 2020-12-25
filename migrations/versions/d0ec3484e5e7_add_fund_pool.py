"""add fund pool

Revision ID: d0ec3484e5e7
Revises: c7d134d215ff
Create Date: 2020-12-25 11:26:43.739653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0ec3484e5e7'
down_revision = 'c7d134d215ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fund_pools',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fund_id', sa.CHAR(length=20), nullable=True),
    sa.Column('pool_type', sa.CHAR(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fund_pools')
    # ### end Alembic commands ###
