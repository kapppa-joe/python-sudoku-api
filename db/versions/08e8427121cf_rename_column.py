"""rename column

Revision ID: 08e8427121cf
Revises: 
Create Date: 2021-12-05 18:43:15.373958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08e8427121cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # pass
    op.alter_column('puzzles', 'score', nullable=False,
                    new_column_name='difficulty')


def downgrade():
    pass
