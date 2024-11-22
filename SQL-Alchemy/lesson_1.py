from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# Define URL
url = URL.create(
    drivername='postgresql+psycopg2',
    username='testuser',
    password='testpassword',
    host='localhost',
    port=5432,
    database='testuser'
)

engine = create_engine(
    url,
    echo=True # logging
)
# Currently this is just a power button, we need to have a connection
# We need a session pool
# When we have a query, it retrieve from session pool.

# The sessionmaker factory generates new Session objects when called, creating them given the configurational arguments established here.
# https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker
Session = sessionmaker(engine)

# Example usecase
# session = Session()
# with Session() as session:
#     session.add(some_object)
#     session.add(some_other_object)
#     session.commit()

with Session() as session:
    session.execute(text("""

"""))

# Run the file to check if it worked