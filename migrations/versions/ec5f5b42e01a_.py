"""empty message

Revision ID: ec5f5b42e01a
Revises: 4abc57c3dc6b
Create Date: 2023-01-05 17:22:48.849184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec5f5b42e01a'
down_revision = '4abc57c3dc6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.BLOB(),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.Text(),
               type_=sa.BLOB(),
               existing_nullable=True)

    # ### end Alembic commands ###
