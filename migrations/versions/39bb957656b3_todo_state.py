"""todo_state

Revision ID: 39bb957656b3
Revises: f6ddfdd212f7
Create Date: 2021-08-16 11:03:33.521595

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker


# revision identifiers, used by Alembic.
revision = '39bb957656b3'
down_revision = 'f6ddfdd212f7'
branch_labels = None
depends_on = None

Session = sessionmaker()


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute('''ALTER TABLE todo ADD COLUMN state text null;''')

    session.execute('''UPDATE todo set state='PENDING';''')
    session.execute('''UPDATE todo set state='CANCELED' WHERE canceled=true;''')
    session.execute('''UPDATE todo set state='COMPLETED' WHERE finished_at IS NOT NULL AND canceled=false;''')

    op.drop_column('todo', 'canceled')

    session.execute('''ALTER TABLE todo ALTER COLUMN state SET NOT NULL;''')
    session.execute('''ALTER TABLE todo ALTER COLUMN text SET NOT NULL;''')
    session.execute('''ALTER TABLE todo ALTER COLUMN created_at SET NOT NULL;''')
    # ### end Alembic commands ###


def downgrade():
    raise Exception('no going back :((')
