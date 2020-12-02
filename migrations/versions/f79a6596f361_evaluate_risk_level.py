"""evaluate risk level

Revision ID: f79a6596f361
Revises: 2fb06a9f2264
Create Date: 2020-12-02 14:45:34.583045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f79a6596f361'
down_revision = '2fb06a9f2264'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eval_answers',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('answer', sa.VARCHAR(length=63), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('risk_level', sa.CHAR(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('eval_questions',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_num', sa.Integer(), nullable=True),
    sa.Column('question', sa.VARCHAR(length=255), nullable=True),
    sa.Column('symbol', sa.VARCHAR(length=32), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('score', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eval_questions')
    op.drop_table('eval_answers')
    # ### end Alembic commands ###