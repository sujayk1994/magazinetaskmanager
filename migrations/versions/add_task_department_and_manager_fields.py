"""add task department and manager fields

Revision ID: add_task_dept_mgr
Revises: c76bd2127030
Create Date: 2025-11-20

"""
from alembic import op
import sqlalchemy as sa


revision = 'add_task_dept_mgr'
down_revision = 'd8e3f520a9b2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_manager', sa.Boolean(), nullable=True, server_default='0'))
    
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assigned_department', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('original_requester_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_task_original_requester', 'users', ['original_requester_id'], ['id'])


def downgrade():
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_constraint('fk_task_original_requester', type_='foreignkey')
        batch_op.drop_column('original_requester_id')
        batch_op.drop_column('assigned_department')
    
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_manager')
