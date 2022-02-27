"""add foregin key to posts table

Revision ID: 0f1255f3eb3a
Revises: a5712a035e04
Create Date: 2022-02-26 17:07:47.972659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f1255f3eb3a'
down_revision = 'a5712a035e04'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'],
                           remote_cols=['id'], ondelete='CASCADE')

def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')

