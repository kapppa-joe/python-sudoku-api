"""puzzles table

Revision ID: 5851ff423906
Revises: 
Create Date: 2021-12-02 20:38:39.404171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5851ff423906'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('puzzles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('puzzle', sa.Text(), nullable=False),
    sa.Column('solution', sa.Text(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('size', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('puzzles')
    # ### end Alembic commands ###
