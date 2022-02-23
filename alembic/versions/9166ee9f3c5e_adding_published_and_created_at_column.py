""" adding published and created at column

Revision ID: 9166ee9f3c5e
Revises: 3a3541303843
Create Date: 2022-02-17 16:52:03.530673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9166ee9f3c5e'
down_revision = '3a3541303843'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
