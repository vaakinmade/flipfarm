"""altered cycle to fund_status on commodity table

Revision ID: 94da65eb541c
Revises: dfc51393bedd
Create Date: 2023-01-08 11:23:08.058600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94da65eb541c'
down_revision = 'dfc51393bedd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commodity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fund_status', sa.String(length=50), nullable=True))
        batch_op.drop_index('ix_commodity_cycle')
        batch_op.drop_column('cycle')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commodity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cycle', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_index('ix_commodity_cycle', ['cycle'], unique=False)
        batch_op.drop_column('fund_status')

    # ### end Alembic commands ###
