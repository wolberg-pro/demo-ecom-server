"""update user and bind if need to store

Revision ID: aace8b1bfe38
Revises: 4add0ba749bc
Create Date: 2021-05-25 18:18:34.286887

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aace8b1bfe38'
down_revision = '4add0ba749bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('users', sa.Column('from_store_id', sa.INTEGER(), sa.ForeignKey('stores.id'),
                                     nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_constraint('stores_from_store_id_fkey', 'user_roles', type_='foreignkey')
    op.drop_column('users', 'from_store_id')
    # ### end Alembic commands ###