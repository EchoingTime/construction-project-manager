"""Added Task table and connected it to Project table

Revision ID: 429ea895e98d
Revises: 8ddd3a94703a
Create Date: 2025-03-30 13:22:41.649328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '429ea895e98d'
down_revision = '8ddd3a94703a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(timezone=True), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('deadline', sa.Date(), nullable=True),
    sa.Column('completion', sa.Enum('Completed', 'In Progress', 'Canceled', name='completion_status'), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###
