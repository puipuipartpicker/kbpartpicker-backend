from alembic import op
from sqlalchemy.dialects import postgresql


stabilizer_type = postgresql.ENUM('pcb_screw_in', 'pcb_snap_in', 'plate_mount', name='stabilizer_type')
layout_type = postgresql.ENUM('forty_percent', 'sixty_percent', 'sixtyfive_percent', 'seventyfive_percent', 'tenkeyless', 'winkeyless', 'hhkb', 'full_size', name='layout_type')
size_type = postgresql.ENUM('six_point_25_u', 'seven_u', 'two_u', name='size_type')
product_type = postgresql.ENUM('switch', 'case', 'pcb', 'plate', 'keyset', name='product_type')
stabilizer_type.create(op.get_bind())
layout_type.create(op.get_bind())
size_type.create(op.get_bind())
product_type.create(op.get_bind())