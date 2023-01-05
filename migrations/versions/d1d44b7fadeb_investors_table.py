"""investors table

Revision ID: d1d44b7fadeb
Revises: 
Create Date: 2022-12-24 13:17:28.654274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1d44b7fadeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('investor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('investor', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_investor_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_investor_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_investor_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_investor_last_name'), ['last_name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('investor', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_investor_last_name'))
        batch_op.drop_index(batch_op.f('ix_investor_first_name'))
        batch_op.drop_index(batch_op.f('ix_investor_email'))
        batch_op.drop_index(batch_op.f('ix_investor_created_at'))

    op.drop_table('investor')
    # ### end Alembic commands ###
