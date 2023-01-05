"""changed user_id to investor_id on investment table

Revision ID: 85b0eac7f6f8
Revises: 7c8928113c9a
Create Date: 2022-12-30 20:13:30.842972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85b0eac7f6f8'
down_revision = '7c8928113c9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('investor_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('investment_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'investor', ['investor_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('investment_user_id_fkey', 'investor', ['user_id'], ['id'])
        batch_op.drop_column('investor_id')

    # ### end Alembic commands ###