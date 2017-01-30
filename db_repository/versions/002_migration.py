from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
node__data = Table('node__data', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('timestamp', VARCHAR(length=30)),
    Column('data_co2', VARCHAR(length=15)),
    Column('data_temp', VARCHAR(length=15)),
    Column('data_hum', VARCHAR(length=15)),
    Column('data_light', VARCHAR(length=15)),
)

data = Table('data', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', String(length=30)),
    Column('data_co2', String(length=15)),
    Column('data_temp', String(length=15)),
    Column('data_hum', String(length=15)),
    Column('data_light', String(length=15)),
    Column('node_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['node__data'].drop()
    post_meta.tables['data'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['node__data'].create()
    post_meta.tables['data'].drop()
