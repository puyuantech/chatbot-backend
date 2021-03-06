"""[fix] wx id

Revision ID: a3ab3ccaa39b
Revises: b5dbe1db312c
Create Date: 2020-11-30 10:32:03.366689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3ab3ccaa39b'
down_revision = 'b5dbe1db312c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_wx_ibfk_1', 'user_wx', type_='foreignkey')
    op.create_foreign_key(None, 'user_wx', 'chatbot_user_info', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_wx', type_='foreignkey')
    op.create_foreign_key('user_wx_ibfk_1', 'user_wx', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
