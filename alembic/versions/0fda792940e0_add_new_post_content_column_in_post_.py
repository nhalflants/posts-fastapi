"""add new post content column in post table

Revision ID: 0fda792940e0
Revises: fbd8ee385be5
Create Date: 2023-02-16 14:21:26.020800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fda792940e0'
down_revision = 'fbd8ee385be5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
