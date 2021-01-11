"""empty message

Revision ID: 998e3d1a0918
Revises: 9867cfc8fa97
Create Date: 2021-01-11 23:18:08.273802

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '998e3d1a0918'
down_revision = '9867cfc8fa97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('layout_type', postgresql.ENUM('forty_percent', 'sixty_percent', 'sixtyfive_percent', 'seventyfive_percent', 'tenkeyless', 'winkeyless', 'frowless', 'full_size', name='layout_type'), nullable=True))
    op.add_column('products', sa.Column('size_type', postgresql.ENUM('six_point_25_u', 'seven_u', 'two_u', 'sixty_kit', 'full_kit', name='size_type'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'size_type')
    op.drop_column('products', 'layout_type')
    # ### end Alembic commands ###
