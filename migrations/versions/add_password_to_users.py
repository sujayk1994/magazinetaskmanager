"""add password to users

Revision ID: add_password_column
Revises: 126b14e153e3
Create Date: 2025-11-21 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


revision = 'add_password_column'
down_revision = '126b14e153e3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('password', sa.String(length=255), nullable=True))
    
    connection = op.get_bind()
    connection.execute(
        sa.text(f"UPDATE users SET password = :password"),
        {"password": generate_password_hash('password123')}
    )


def downgrade():
    op.drop_column('users', 'password')
