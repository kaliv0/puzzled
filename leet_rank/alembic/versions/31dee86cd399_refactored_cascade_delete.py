"""Refactored cascade delete

Revision ID: 31dee86cd399
Revises: aed609fc7feb
Create Date: 2023-11-02 16:10:21.895705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31dee86cd399'
down_revision: Union[str, None] = 'aed609fc7feb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_descriptions')
    op.drop_table('tasks')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tasks_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tasks_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('task_descriptions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='task_descriptions_task_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='task_descriptions_pkey')
    )
    # ### end Alembic commands ###