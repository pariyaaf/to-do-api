"""empty message

Revision ID: 1261745219d9
Revises: b61fd97cb4bb
Create Date: 2024-06-08 19:29:47.379891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1261745219d9'
down_revision = 'b61fd97cb4bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('due_date',
               existing_type=sa.BOOLEAN(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('due_date',
               existing_type=sa.Date(),
               type_=sa.BOOLEAN(),
               existing_nullable=True)

    # ### end Alembic commands ###
