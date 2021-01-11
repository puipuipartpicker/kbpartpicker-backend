"""empty message

Revision ID: bac32b1089aa
Revises: 16754cde33c8
Create Date: 2021-01-06 17:32:41.707791

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bac32b1089aa'
down_revision = '16754cde33c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('countries', 'country_code',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('countries', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('countries', 'currency_code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('countries', 'exchange_rate',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('countries', 'iso_code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('countries', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.alter_column('countries', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('countries', 'iso_code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('countries', 'exchange_rate',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('countries', 'currency_code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('countries', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('countries', 'country_code',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###