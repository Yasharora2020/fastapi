"""adding votes table

Revision ID: 17f18e44ad1e
Revises: 9166ee9f3c5e
Create Date: 2022-02-18 09:06:17.913605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17f18e44ad1e'
down_revision = '9166ee9f3c5e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )


def downgrade():
    op.drop_table('votes')
