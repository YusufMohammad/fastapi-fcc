"""Add content column to posts table

Revision ID: a6ac04132382
Revises: 8add7b9f73d9
Create Date: 2022-01-23 03:45:08.176662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6ac04132382'
down_revision = '8add7b9f73d9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
