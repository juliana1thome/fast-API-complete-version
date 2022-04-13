"""Create Posts Table

Revision ID: 86263554e7d8
Revises:
Create Date: 2022-04-13 13:00:45.255701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86263554e7d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False), sa.Column('content', sa.String(), nullable=False), sa.Column('published', sa.BOOLEAN(), server_default='True', nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
