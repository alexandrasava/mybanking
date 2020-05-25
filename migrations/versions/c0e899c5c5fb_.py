"""empty message

Revision ID: c0e899c5c5fb
Revises: 
Create Date: 2020-04-06 08:11:58.063276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0e899c5c5fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchanges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=24, scale=8), nullable=False),
    sa.Column('exchange_rate', sa.DECIMAL(precision=24, scale=8), nullable=False),
    sa.Column('amount_usd', sa.DECIMAL(precision=24, scale=8), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exchanges_creation_date'), 'exchanges', ['creation_date'], unique=False)
    op.create_index(op.f('ix_exchanges_currency'), 'exchanges', ['currency'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_exchanges_currency'), table_name='exchanges')
    op.drop_index(op.f('ix_exchanges_creation_date'), table_name='exchanges')
    op.drop_table('exchanges')
    # ### end Alembic commands ###