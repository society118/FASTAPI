from typing import Annotated
from sqlalchemy.ext.asyncio import  create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from fastapi import FastAPI,Depends
import uvicorn
from pydantic import BaseModel
app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db')
new_session =async_sessionmaker(engine,expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession,Depends(get_session)]

class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "books"
    id:Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

class BookAddSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookAddSchema):
    id:int



@app.post("/setup_database/")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"status": "database recreated"}

@app.get("/books")
async def get_books():
    pass

@app.post("/books")
async def add_books(data:BookSchema,session:SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"ok":True}



if __name__ =='__main__':
    uvicorn.run("main1:app",reload=True,port=5052)