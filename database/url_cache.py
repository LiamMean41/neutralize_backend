import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import Table, Column, Text, MetaData, select
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///database/SQLite.db"

engine = _sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

conn = engine.connect()

metadata = MetaData()

# Define the Cache table
website_cache = Table(
    "Cache", metadata,
    Column("url", Text, primary_key=True, unique=True, nullable=False),
    Column("title", Text, nullable=False),
    Column("text", Text, nullable=False)
)

# Create the table if it doesn't exist
metadata.create_all(engine)

# Initialize FastAPI
app = FastAPI()

# Request model
class CacheRequest(BaseModel):
    url: str
    title: str
    text: str

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cache")
async def check_and_insert_cache(request: CacheRequest, db=Depends(get_db)):
    """Checks if the URL exists in the cache. If not, inserts it."""
    
    query = select(website_cache.c.url, website_cache.c.title, website_cache.c.text).where(website_cache.c.url == request.url)
    result = db.execute(query).fetchone()

    if result:
        return {"message": "Data retrieved from cache", "data": {"url": result[0], "title": result[1], "text": result[2]}}

    # Insert new data
    db.execute(website_cache.insert().values(url=request.url, title=request.title, text=request.text))
    db.commit()

    return {"message": "Data inserted into cache", "data": request.dict()}
