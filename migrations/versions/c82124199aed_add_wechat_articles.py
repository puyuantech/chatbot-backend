"""Add Wechat articles

Revision ID: c82124199aed
Revises: a426e738743c
Create Date: 2020-12-30 14:28:38.538377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c82124199aed'
down_revision = 'a426e738743c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wechat_article',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wxid', sa.CHAR(length=128), nullable=True),
    sa.Column('wxname', sa.CHAR(length=128), nullable=True),
    sa.Column('doc_id', sa.CHAR(length=16), nullable=True),
    sa.Column('seq', sa.Integer(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('cover', sa.Text(), nullable=True),
    sa.Column('doc_ct', sa.DATETIME(), nullable=True),
    sa.Column('read', sa.Integer(), nullable=True),
    sa.Column('like', sa.Integer(), nullable=True),
    sa.Column('click_ts', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wechat_public_account',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wxname', sa.CHAR(length=128), nullable=True),
    sa.Column('wxid', sa.CHAR(length=128), nullable=True),
    sa.Column('account_owner', sa.Text(), nullable=True),
    sa.Column('account_type', sa.CHAR(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('importance', sa.Integer(), nullable=True),
    sa.Column('crawled', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wechat_public_account')
    op.drop_table('wechat_article')
    # ### end Alembic commands ###