"""Create posts table

Revision ID: 8add7b9f73d9
Revises: 
Create Date: 2022-01-23 03:32:09.098345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8add7b9f73d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
