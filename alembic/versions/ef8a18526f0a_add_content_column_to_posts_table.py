"""add content column to posts table

Revision ID: ef8a18526f0a
Revises: 3132028b2974
Create Date: 2022-02-17 16:36:49.318911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef8a18526f0a'
down_revision = '3132028b2974'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
