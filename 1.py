import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app =FastAPI()

books =[
    {
        "id":1,
        "title": "Асинхронность в пайтон",
        "author": "Метти",
    },
    {"id": 2,
     "title":"backebd developer of python",
     "author":"Артем",
    },
]
@app.get("/books/",tags=["книги"],summary="Получить конкретную книгу")
def read_books():
    return books

@app.get("/books/{book_id}",tags=["книги"])
def get_books(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Not Found")

class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books/",tags=["книги"])
def create_book(new_book:NewBook):
    books.append({
        "title":new_book.title,
        "author":new_book.author,
        "id":len(books) + 1
    })
    return {"success":True}



if __name__ =='__main__':
    uvicorn.run("1:app",reload=True)