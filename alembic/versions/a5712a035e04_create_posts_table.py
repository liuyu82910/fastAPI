"""create posts  table

Revision ID: a5712a035e04
Revises: 3e17b008418d
Create Date: 2022-02-26 17:05:21.062366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5712a035e04'
down_revision = '3e17b008418d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
                    sa.Column('created_dt', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))

def downgrade():
    op.drop_table('posts')
