"""Add foreign-key to posts table

Revision ID: ffd43391ba46
Revises: 34dc530c88b1
Create Date: 2022-01-23 04:03:31.800402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffd43391ba46'
down_revision = '34dc530c88b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'author_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['author_id'],
                          remote_cols=['id'],  ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name='posts')
    op.drop_column('posts', 'author_id')
    pass
