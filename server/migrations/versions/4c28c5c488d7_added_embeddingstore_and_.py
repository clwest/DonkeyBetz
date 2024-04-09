"""Added EmbeddingStore and CollectionStore to match Langchain

Revision ID: 4c28c5c488d7
Revises: e14e044b2fab
Create Date: 2024-04-09 13:31:42.251413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c28c5c488d7'
down_revision = 'e14e044b2fab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('langchain_pg_collection', schema=None) as batch_op:
        batch_op.add_column(sa.Column('project_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'projects', ['project_id'], ['id'])

    with op.batch_alter_table('langchain_pg_embedding', schema=None) as batch_op:
        batch_op.alter_column('collection_id',
               existing_type=sa.UUID(),
               nullable=False)
        batch_op.drop_column('custom_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('langchain_pg_embedding', schema=None) as batch_op:
        batch_op.add_column(sa.Column('custom_id', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.alter_column('collection_id',
               existing_type=sa.UUID(),
               nullable=True)

    with op.batch_alter_table('langchain_pg_collection', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('project_id')

    # ### end Alembic commands ###