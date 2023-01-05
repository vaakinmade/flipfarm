"""altered active to status on investment table

Revision ID: dfc51393bedd
Revises: dd0131090059
Create Date: 2023-01-02 23:44:45.316400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfc51393bedd'
down_revision = 'dd0131090059'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=True))
        batch_op.drop_column('active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('status')

    # ### end Alembic commands ###
