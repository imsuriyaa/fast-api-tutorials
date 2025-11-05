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

# Path Parameters
@app.get('/books/title/{book_title}')
async def read_all_books(book_title):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book
    return {"message": f"Book with title {book_title} not found"}

# Query Parameter
@app.get('/books/')
async def read_books_by_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    if books_to_return:
        return books_to_return
    else:
        return {'messgae': f"Books in category: {category} not found"}


# Filtering based on both Path and Query Parameter
@app.get('/books/author/{book_author}')
async def read_book_by_author_and_category(book_author: str, category: str):
    books_to_return = []
    print("Inside Read Book by Author and Category")
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category') == category.casefold():
            books_to_return.append(book)
        
    if books_to_return:
        return books_to_return
    else:
        return {'messgae': f"Book not found of the category: {category} by the author {book_author}"}


@app.get('/hello-world')
# async is fairly optional for 
async def hello_world():
    return {"message": "Hello World!"}
