"""merge heads before adding xp

Revision ID: 06d662b5400c
Revises: 38083713f2c9, add_xp_level_progress
Create Date: 2025-11-19 14:09:00.499206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06d662b5400c'
down_revision = ('38083713f2c9', 'add_xp_level_progress')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
