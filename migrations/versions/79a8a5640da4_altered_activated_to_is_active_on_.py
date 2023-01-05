"""altered_activated_to_is_active_on_investor table

Revision ID: 79a8a5640da4
Revises: a3464c855f38
Create Date: 2022-12-27 15:38:23.599458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79a8a5640da4'
down_revision = 'a3464c855f38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))
        batch_op.drop_column('activated')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('activated', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
