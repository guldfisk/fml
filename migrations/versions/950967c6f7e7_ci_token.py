"""empty message

Revision ID: 950967c6f7e7
Revises: 39bb957656b3
Create Date: 2021-10-15 12:13:40.739514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "950967c6f7e7"
down_revision = "39bb957656b3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ci_token",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=127), nullable=False),
        sa.Column("value", sa.String(length=127), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("ci_token")
