"""generate votes tables

Revision ID: ca6426da1b03
Revises: 4d8d326d8524
Create Date: 2023-02-16 14:43:28.147203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca6426da1b03'
down_revision = '4d8d326d8524'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id'))


def downgrade() -> None:
    op.drop_table('votes')
