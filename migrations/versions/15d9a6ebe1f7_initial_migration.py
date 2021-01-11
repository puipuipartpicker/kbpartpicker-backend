"""Initial migration.

Revision ID: 15d9a6ebe1f7
Revises: 
Create Date: 2021-01-06 17:31:16.736624

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '15d9a6ebe1f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('country_name', sa.String(), nullable=False),
    sa.Column('country_code', sa.Integer(), nullable=False),
    sa.Column('iso_code', sa.String(), nullable=False),
    sa.Column('currency_code', sa.String(), nullable=False),
    sa.Column('exchange_rate', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('country')
    op.add_column('products', sa.Column('stabilizer_type', sa.Enum('pcb_screw_in', 'pcb_snap_in', 'plate_mount', name='stabilizertype'), nullable=True))
    op.alter_column('products', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('products', 'img_url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('products', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('vendor_product_associations', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('vendor_product_associations', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('vendor_product_associations', 'url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('vendors', 'country_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('vendors', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('vendors', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_constraint('vendors_country_id_fkey', 'vendors', type_='foreignkey')
    op.create_foreign_key(None, 'vendors', 'countries', ['country_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vendors', type_='foreignkey')
    op.create_foreign_key('vendors_country_id_fkey', 'vendors', 'country', ['country_id'], ['id'])
    op.alter_column('vendors', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('vendors', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('vendors', 'country_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('vendor_product_associations', 'url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('vendor_product_associations', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('vendor_product_associations', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('products', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('products', 'img_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('products', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('products', 'stabilizer_type')
    op.create_table('country',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('country_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('country_code', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('iso_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('currency_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('exchange_rate', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='country_pkey')
    )
    op.drop_table('countries')
    # ### end Alembic commands ###