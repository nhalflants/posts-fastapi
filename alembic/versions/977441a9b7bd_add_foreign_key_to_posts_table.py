"""add foreign key to posts table

Revision ID: 977441a9b7bd
Revises: c7338785d53a
Create Date: 2023-02-16 14:32:15.943502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '977441a9b7bd'
down_revision = 'c7338785d53a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
