"""comments

Revision ID: 78bc7345edfb
Revises: 2a8d08a2c5ad
Create Date: 2021-04-06 13:36:20.585985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78bc7345edfb'
down_revision = '2a8d08a2c5ad'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=127), nullable=False),
    sa.Column('todo_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['todo_id'], ['todo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('comment')
