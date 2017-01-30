from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
node = Table('node', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('desc', VARCHAR(length=100)),
    Column('pos', VARCHAR(length=20)),
    Column('last', VARCHAR(length=30)),
)

node = Table('node', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('desc', String(length=100)),
    Column('pos', String(length=20)),
    Column('last_time', String(length=30)),
    Column('last_dataid', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['node'].columns['last'].drop()
    post_meta.tables['node'].columns['last_dataid'].create()
    post_meta.tables['node'].columns['last_time'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['node'].columns['last'].create()
    post_meta.tables['node'].columns['last_dataid'].drop()
    post_meta.tables['node'].columns['last_time'].drop()
