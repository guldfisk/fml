"""deferable_priority_level

Revision ID: 5de737f1af94
Revises: 41fad22aac92
Create Date: 2021-02-16 13:52:45.510079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de737f1af94'
down_revision = '41fad22aac92'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('priority_project_id_level_key', 'priority', type_ = 'unique')
    op.create_unique_constraint(None, 'priority', ['project_id', 'level'], deferrable = True)


def downgrade():
    pass
