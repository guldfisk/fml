"""unique_tags

Revision ID: 7e69469f0fa8
Revises: 53012f51cfea
Create Date: 2021-02-02 15:43:42.498736

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "7e69469f0fa8"
down_revision = "53012f51cfea"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "tag", ["text"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tag", type_="unique")
    # ### end Alembic commands ###
