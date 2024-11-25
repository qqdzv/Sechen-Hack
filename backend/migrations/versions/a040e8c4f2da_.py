"""empty message

Revision ID: a040e8c4f2da
Revises: efa10d726c86
Create Date: 2024-11-03 16:58:48.489424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a040e8c4f2da'
down_revision: Union[str, None] = 'efa10d726c86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ai_message', sa.Column('ai_answer', sa.String(), nullable=True))
    op.drop_column('ai_message', 'receiver_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ai_message', sa.Column('receiver_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('ai_message', 'ai_answer')
    # ### end Alembic commands ###
