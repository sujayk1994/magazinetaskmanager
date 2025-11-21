"""Add task ownership columns

Revision ID: 126b14e153e3
Revises: be5bbf15a53f
Create Date: 2025-11-21 11:20:35

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '126b14e153e3'
down_revision = 'be5bbf15a53f'
branch_labels = None
depends_on = None


def upgrade():
    # Add editorial_owner_id and design_owner_id columns to tasks table
    op.add_column('tasks', sa.Column('editorial_owner_id', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('design_owner_id', sa.Integer(), nullable=True))
    
    # Add foreign key constraints
    op.create_foreign_key('fk_tasks_editorial_owner', 'tasks', 'users', ['editorial_owner_id'], ['id'])
    op.create_foreign_key('fk_tasks_design_owner', 'tasks', 'users', ['design_owner_id'], ['id'])


def downgrade():
    # Drop foreign key constraints
    op.drop_constraint('fk_tasks_design_owner', 'tasks', type_='foreignkey')
    op.drop_constraint('fk_tasks_editorial_owner', 'tasks', type_='foreignkey')
    
    # Drop columns
    op.drop_column('tasks', 'design_owner_id')
    op.drop_column('tasks', 'editorial_owner_id')
