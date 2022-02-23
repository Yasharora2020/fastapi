""" adding phone number

Revision ID: 6b6d6a91203b
Revises: 17f18e44ad1e
Create Date: 2022-02-18 09:09:37.275678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b6d6a91203b'
down_revision = '17f18e44ad1e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'phone_number')
