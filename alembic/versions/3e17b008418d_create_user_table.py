"""create user table

Revision ID: 3e17b008418d
Revises: 
Create Date: 2022-02-26 17:04:44.141943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e17b008418d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_dt', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.UniqueConstraint('email'))

def downgrade():
    op.drop_table('users')
