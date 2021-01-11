"""empty message

Revision ID: 94522daf9562
Revises: a6df4c9ca7af
Create Date: 2021-01-11 23:20:56.396437

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '94522daf9562'
down_revision = 'a6df4c9ca7af'
branch_labels = None
depends_on = None


def upgrade():
    layout_type = postgresql.ENUM('forty_percent', 'sixty_percent', 'sixtyfive_percent', 'seventyfive_percent', 'tenkeyless', 'winkeyless', 'hhkb', 'full_size', name='layout_type')
    size_type = postgresql.ENUM('six_point_25_u', 'seven_u', 'two_u', name='size_type')
    layout_type.create(op.get_bind())
    size_type.create(op.get_bind())
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('layout_type', layout_type, nullable=True))
    op.add_column('products', sa.Column('size_type', size_type, nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'size_type')
    op.drop_column('products', 'layout_type')
    # ### end Alembic commands ###
