"""Se agregan cantidad y tipo de empaque

Revision ID: dc14f0bbacbe
Revises: 5febed99ae4d
Create Date: 2024-01-23 15:06:21.065093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc14f0bbacbe'
down_revision = '5febed99ae4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parcel_type',
    sa.Column('paty_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('paty_desc', sa.String(length=100), nullable=False),
    sa.Column('paty_created_at', sa.DateTime(), nullable=True),
    sa.Column('paty_user_created_id', sa.Integer(), nullable=False),
    sa.Column('paty_updated_at', sa.DateTime(), nullable=True),
    sa.Column('paty_user_updated_id', sa.Integer(), nullable=True),
    sa.Column('paty_state', sa.String(length=1), nullable=False),
    sa.ForeignKeyConstraint(['paty_user_created_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['paty_user_updated_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('paty_id'),
    sa.UniqueConstraint('paty_desc')
    )
    with op.batch_alter_table('people_prescription_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prde_paty_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('prde_quantity', sa.Integer(), nullable=False))
        batch_op.create_foreign_key("fk_prde_paty_id", 'parcel_type', ['prde_paty_id'], ['paty_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people_prescription_details', schema=None) as batch_op:
        batch_op.drop_constraint('fk_prde_paty_id', type_='foreignkey')
        batch_op.drop_column('prde_quantity')
        batch_op.drop_column('prde_paty_id')

    op.drop_table('parcel_type')
    # ### end Alembic commands ###
