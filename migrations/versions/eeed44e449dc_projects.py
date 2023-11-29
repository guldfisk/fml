"""projects

Revision ID: eeed44e449dc
Revises: b047b954e461
Create Date: 2021-02-03 14:26:32.302201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eeed44e449dc"
down_revision = "b047b954e461"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=127), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("project")
    # ### end Alembic commands ###
