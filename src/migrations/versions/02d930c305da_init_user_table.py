"""init user table

Revision ID: 02d930c305da
Revises: 
Create Date: 2021-05-11 12:34:27.690397

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '02d930c305da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('uid', sa.String(length=100), unique=True, index=True, nullable=False),
                    sa.Column('avatar_id', sa.Integer(), nullable=True),
                    sa.Column('phone', sa.String(length=100), nullable=True),
                    sa.Column('address1', sa.String(length=100), nullable=True),
                    sa.Column('address2', sa.String(length=100), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('create_at', sa.DateTime(), default=sa.func.current_timestamp()),
                    sa.Column('update_at', sa.DateTime(), onupdate=sa.ColumnDefault(sa.func.current_timestamp), default=sa.func.current_timestamp()),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
