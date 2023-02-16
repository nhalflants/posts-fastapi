"""create posts table

Revision ID: fbd8ee385be5
Revises: 
Create Date: 2023-02-16 14:12:50.993402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbd8ee385be5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", \
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True), \
        sa.Column("title", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table("posts")
