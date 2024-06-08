from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

DATABASE_CONNECTION_STRING = settings.database_connection_string

engine = create_engine(DATABASE_CONNECTION_STRING)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi-socialmedia', user='postgres', password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print(f"connecting to database failed. Error: {error}")
#         time.sleep(2)