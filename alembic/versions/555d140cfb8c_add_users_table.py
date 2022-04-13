"""Add users table

Revision ID: 555d140cfb8c
Revises: 86263554e7d8
Create Date: 2022-04-13 13:36:05.489949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '555d140cfb8c'
down_revision = '86263554e7d8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
