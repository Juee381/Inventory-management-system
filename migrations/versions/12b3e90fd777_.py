"""empty message

Revision ID: 12b3e90fd777
Revises: f16b11096467
Create Date: 2023-01-05 12:21:29.861466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12b3e90fd777'
down_revision = 'f16b11096467'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.BLOB(),
               type_=sa.Text(),
               nullable=False)
        batch_op.create_unique_constraint(None, ['image'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('image',
               existing_type=sa.Text(),
               type_=sa.BLOB(),
               nullable=True)

    # ### end Alembic commands ###
