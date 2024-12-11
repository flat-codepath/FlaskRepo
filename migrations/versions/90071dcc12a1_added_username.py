"""added username

Revision ID: 90071dcc12a1
Revises: f69d392eea33
Create Date: 2024-12-11 16:28:34.529342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90071dcc12a1'
down_revision = 'f69d392eea33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=200), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
