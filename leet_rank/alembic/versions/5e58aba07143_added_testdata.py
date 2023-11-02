"""Added testdata

Revision ID: 5e58aba07143
Revises: 83a98dca2270
Create Date: 2023-11-02 17:19:47.103379

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5e58aba07143'
down_revision: Union[str, None] = '83a98dca2270'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_descriptions')
    op.drop_table('tasks')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_descriptions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='task_descriptions_task_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='task_descriptions_pkey')
    )
    op.create_table('tasks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tasks_pkey')
    )
    # ### end Alembic commands ###
