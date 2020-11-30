"""Add wechat group ID in prod view table

Revision ID: 067f3b34e617
Revises: a3ab3ccaa39b
Create Date: 2020-11-30 17:36:15.204193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '067f3b34e617'
down_revision = 'a3ab3ccaa39b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chatbot_product_view', sa.Column('wechat_group_id', sa.CHAR(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chatbot_product_view', 'wechat_group_id')
    # ### end Alembic commands ###
