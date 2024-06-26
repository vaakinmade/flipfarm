"""user_id and commodity_id fk on investments table

Revision ID: 468795f73844
Revises: aac7f7bc05d4
Create Date: 2022-12-24 13:34:40.357208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '468795f73844'
down_revision = 'aac7f7bc05d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('commodity_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'commodity', ['commodity_id'], ['id'])
        batch_op.create_foreign_key(None, 'investor', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('commodity_id')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
