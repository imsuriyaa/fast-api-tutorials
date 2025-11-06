from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class BookRequest(BaseModel):
    # if id is not passed it won't raise an error
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999,lt=2026)

    model_config = {
        "json_schema_extra": {
            "title": "A new book",
            "author": "Code with Suriyaa",
            "description": "A new description",
            "rating": 5
        }
    }




class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2010),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2010),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2019),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2018),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2017),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2016)
]


@app.get('/',status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get('/books/{book_id}',status_code=status.HTTP_200_OK)
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
    raise HTTPException(status_code=404, detail='Item not found')

@app.get('/books/byrating/',status_code=status.HTTP_200_OK)
async def fetch_books_byrating(book_rating: int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    if  books_to_return:
        return books_to_return
    raise HTTPException(status_code=404, detail='Item not found')

@app.get('/books/by-published-year/{published_year}', status_code=status.HTTP_200_OK)
async def fetch_by_published_year(published_year: int = Path(gt=1999,lt=2026)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_year:
            books_to_return.append(book)
    
    if books_to_return:
        return books_to_return
    
    raise HTTPException(status_code=404, detail='Item not found')


@app.post('/create-book',status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return BOOKS



def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            book_changed = 1
            BOOKS[i] = book

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete('/books/delete/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int = Path(gt=0)):
    books_changed = 0
    for i in range(len(BOOKS)):
        print(BOOKS[i])
        if BOOKS[i].id == book_id:
            books_changed = 1
            BOOKS.pop(i)
            return
    
    if not books_changed:
        raise HTTPException(status_code=404, detail="Item not found")


