from db import engine
from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar())  # This should print '1' if the connection is successful
