"""Add last few columns to posts table

Revision ID: 0772dc1b358f
Revises: ffd43391ba46
Create Date: 2022-01-23 04:14:47.977289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0772dc1b358f'
down_revision = 'ffd43391ba46'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_on', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_on')
    pass
