"""project_default_priority_filter

Revision ID: 2a8d08a2c5ad
Revises: 5de737f1af94
Create Date: 2021-04-06 09:04:21.103774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a8d08a2c5ad'
down_revision = '5de737f1af94'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('project', sa.Column('default_priority_filter', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('project', 'default_priority_filter')
