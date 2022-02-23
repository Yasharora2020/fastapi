"""create posts table

Revision ID: 3132028b2974
Revises: 
Create Date: 2022-02-17 16:24:10.571694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3132028b2974'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
