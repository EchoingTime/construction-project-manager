"""Add is_invoice column to File model.

Revision ID: 2c6bb178a977
Revises: 3f0a63e2bf25
Create Date: 2025-04-05 17:56:31.310960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c6bb178a977'
down_revision = '3f0a63e2bf25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_invoice', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.drop_column('is_invoice')

    # ### end Alembic commands ###
