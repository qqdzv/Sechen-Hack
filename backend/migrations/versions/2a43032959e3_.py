"""empty message

Revision ID: 2a43032959e3
Revises: 2768264f803e
Create Date: 2024-11-05 13:45:17.680309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a43032959e3'
down_revision: Union[str, None] = '2768264f803e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_ai_message_created_at'), 'ai_message', ['created_at'], unique=False)
    op.create_index(op.f('ix_ai_message_role'), 'ai_message', ['role'], unique=False)
    op.create_index(op.f('ix_ai_message_sender_id'), 'ai_message', ['sender_id'], unique=False)
    op.create_index(op.f('ix_doctor_scan_age'), 'doctor_scan', ['age'], unique=False)
    op.create_index(op.f('ix_doctor_scan_body_part'), 'doctor_scan', ['body_part'], unique=False)
    op.create_index(op.f('ix_doctor_scan_created_at'), 'doctor_scan', ['created_at'], unique=False)
    op.create_index(op.f('ix_doctor_scan_gender'), 'doctor_scan', ['gender'], unique=False)
    op.create_index(op.f('ix_doctor_scan_sender_id'), 'doctor_scan', ['sender_id'], unique=False)
    op.add_column('message', sa.Column('abcd_score', sa.String(), nullable=True))
    op.add_column('message', sa.Column('doctor_result', sa.String(), nullable=True))
    op.create_index(op.f('ix_message_created_at'), 'message', ['created_at'], unique=False)
    op.create_index(op.f('ix_message_receiver_id'), 'message', ['receiver_id'], unique=False)
    op.create_index(op.f('ix_message_receiver_type'), 'message', ['receiver_type'], unique=False)
    op.create_index(op.f('ix_message_sender_id'), 'message', ['sender_id'], unique=False)
    op.create_index(op.f('ix_message_sender_type'), 'message', ['sender_type'], unique=False)
    op.create_index(op.f('ix_scan_contains_skin'), 'scan', ['contains_skin'], unique=False)
    op.create_index(op.f('ix_scan_recommendations'), 'scan', ['recommendations'], unique=False)
    op.create_index(op.f('ix_scan_response'), 'scan', ['response'], unique=False)
    op.create_index(op.f('ix_user_registered_at'), 'user', ['registered_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_registered_at'), table_name='user')
    op.drop_index(op.f('ix_scan_response'), table_name='scan')
    op.drop_index(op.f('ix_scan_recommendations'), table_name='scan')
    op.drop_index(op.f('ix_scan_contains_skin'), table_name='scan')
    op.drop_index(op.f('ix_message_sender_type'), table_name='message')
    op.drop_index(op.f('ix_message_sender_id'), table_name='message')
    op.drop_index(op.f('ix_message_receiver_type'), table_name='message')
    op.drop_index(op.f('ix_message_receiver_id'), table_name='message')
    op.drop_index(op.f('ix_message_created_at'), table_name='message')
    op.drop_column('message', 'doctor_result')
    op.drop_column('message', 'abcd_score')
    op.drop_index(op.f('ix_doctor_scan_sender_id'), table_name='doctor_scan')
    op.drop_index(op.f('ix_doctor_scan_gender'), table_name='doctor_scan')
    op.drop_index(op.f('ix_doctor_scan_created_at'), table_name='doctor_scan')
    op.drop_index(op.f('ix_doctor_scan_body_part'), table_name='doctor_scan')
    op.drop_index(op.f('ix_doctor_scan_age'), table_name='doctor_scan')
    op.drop_index(op.f('ix_ai_message_sender_id'), table_name='ai_message')
    op.drop_index(op.f('ix_ai_message_role'), table_name='ai_message')
    op.drop_index(op.f('ix_ai_message_created_at'), table_name='ai_message')
    # ### end Alembic commands ###
