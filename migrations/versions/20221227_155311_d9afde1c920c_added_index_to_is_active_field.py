"""added index to is_active field

Revision ID: d9afde1c920c
Revises: 79a8a5640da4
Create Date: 2022-12-27 15:53:11.588963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9afde1c920c'
down_revision = '79a8a5640da4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investor', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_investor_is_active'), ['is_active'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investor', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_investor_is_active'))

    # ### end Alembic commands ###
