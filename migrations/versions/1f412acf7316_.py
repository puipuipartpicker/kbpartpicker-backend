"""empty message

Revision ID: 1f412acf7316
Revises: 903891399954
Create Date: 2021-01-06 18:58:46.401489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f412acf7316'
down_revision = '903891399954'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vendor_product_associations', 'url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vendor_product_associations', 'url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
