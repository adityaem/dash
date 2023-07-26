#!/usr/bin/env python
from sqlalchemy import create_engine

user = 'DASHCHAT',
password = 'Dash2023',
account = 'sony',
warehouse = 'SPHEIT',
role = 'CSG',
database = 'FIVETRAN_DATABASE_PRODUCTION',
schema = 'FACEBOOK_DMA_NEW',
engine = create_engine(
    'snowflake://{user}:{password}@{account_identifier}/'.format(
        user=user,
        password=password,
        account_identifier=account,
    )
)
try:
    connection = engine.connect()
    results = connection.execute('select current_version()').fetchone()
    print(results[0])
finally:
    connection.close()
    engine.dispose()