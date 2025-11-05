from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get('/books')
# async is fairly optional for 
async def read_all_books():
    return BOOKS

@app.get('/books/{book_title}')
async def read_all_books(book_tile):
    for book in BOOKS:
        if book['title'] == book_tile:
            return book
    


@app.get('/hello-world')
# async is fairly optional for 
async def hello_world():
    return {"message": "Hello World!"}
