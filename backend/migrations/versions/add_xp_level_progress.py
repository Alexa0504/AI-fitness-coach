"""add xp, level, progress fields"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers
revision = 'add_xp_level_progress'
down_revision = 'efb995addc9e'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('xp', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('level', sa.Integer(), nullable=False, server_default='1'))

    try:
        op.add_column('users', sa.Column('progress_saved_state', JSONB(), server_default='{}'))
    except:
        op.add_column('users', sa.Column('progress_saved_state', sa.Text(), server_default='{}'))

    op.add_column('users', sa.Column('last_progress_update', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('users', 'xp')
    op.drop_column('users', 'level')
    op.drop_column('users', 'progress_saved_state')
    op.drop_column('users', 'last_progress_update')
