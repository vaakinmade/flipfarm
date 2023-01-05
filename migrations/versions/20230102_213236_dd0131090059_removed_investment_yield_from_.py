"""removed investment yield from investment table

Revision ID: dd0131090059
Revises: 5fed209a6fcb
Create Date: 2023-01-02 21:32:36.123054

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dd0131090059'
down_revision = '5fed209a6fcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investment', schema=None) as batch_op:
        batch_op.drop_index('ix_investment_investment_yield')
        batch_op.drop_column('investment_yield')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('investment_yield', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
        batch_op.create_index('ix_investment_investment_yield', ['investment_yield'], unique=False)

    # ### end Alembic commands ###
