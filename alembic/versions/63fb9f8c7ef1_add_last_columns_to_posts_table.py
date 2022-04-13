"""Add last columns to posts table

Revision ID: 63fb9f8c7ef1
Revises: 3f2c2fea9d23
Create Date: 2022-04-13 14:18:47.625562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63fb9f8c7ef1'
down_revision = '3f2c2fea9d23'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
        ('NOW()')),)
pass


def downgrade():
    op.drop_column('posts', 'created_at')
pass
