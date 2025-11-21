"""Add file deletion and history tracking fields

Revision ID: d8e3f520a9b2
Revises: c76bd2127030
Create Date: 2025-11-20 11:25:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'd8e3f520a9b2'
down_revision = 'c76bd2127030'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('task_files', schema=None) as batch_op:
        batch_op.add_column(sa.Column('history_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('is_deleted', sa.Boolean(), nullable=True, server_default='0'))
        batch_op.create_foreign_key('fk_task_files_history_id', 'task_history', ['history_id'], ['id'])


def downgrade():
    with op.batch_alter_table('task_files', schema=None) as batch_op:
        batch_op.drop_constraint('fk_task_files_history_id', type_='foreignkey')
        batch_op.drop_column('is_deleted')
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('history_id')
