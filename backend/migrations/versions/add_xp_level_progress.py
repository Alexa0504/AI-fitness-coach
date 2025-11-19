"""add xp, level, progress_saved_state to users

Revision ID: add_xp_level_progress
Revises: efb995addc9e_create_users_table
Create Date: 2025-11-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_xp_level_progress'
down_revision = 'efb995addc9e'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    dialect = conn.dialect.name

    op.add_column('users', sa.Column('xp', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('level', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('users', sa.Column('last_progress_update', sa.DateTime(), nullable=True))
    if dialect == 'postgresql':
        op.add_column('users', sa.Column('progress_saved_state', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
        op.execute("UPDATE users SET progress_saved_state = '{}'::jsonb WHERE progress_saved_state IS NULL;")
    else:
        op.add_column('users', sa.Column('progress_saved_state', sa.Text(), nullable=True))
        op.execute("UPDATE users SET progress_saved_state = '{}' WHERE progress_saved_state IS NULL;")

def downgrade():
    op.drop_column('users', 'progress_saved_state')
    op.drop_column('users', 'last_progress_update')
    op.drop_column('users', 'level')
    op.drop_column('users', 'xp')
