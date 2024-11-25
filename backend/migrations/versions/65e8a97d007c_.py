"""empty message

Revision ID: 65e8a97d007c
Revises: 2d4226341c50
Create Date: 2024-11-01 15:46:04.335606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65e8a97d007c'
down_revision: Union[str, None] = '2d4226341c50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('age', sa.String(), nullable=True))
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'gender',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index('ix_user_middle_name', table_name='user')
    op.drop_index('ix_user_role', table_name='user')
    op.create_index(op.f('ix_user_gender'), 'user', ['gender'], unique=False)
    op.drop_column('user', 'middle_name')
    op.drop_column('user', 'tg_id')
    op.drop_column('user', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('tg_id', sa.BIGINT(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('middle_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_user_gender'), table_name='user')
    op.create_index('ix_user_role', 'user', ['role'], unique=False)
    op.create_index('ix_user_middle_name', 'user', ['middle_name'], unique=False)
    op.alter_column('user', 'gender',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('user', 'age')
    # ### end Alembic commands ###