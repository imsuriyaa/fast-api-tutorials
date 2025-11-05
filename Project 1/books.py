from fastapi import FastAPI

app = FastAPI()

@app.get('/')
# async is fairly optional for 
async def hello_world():
    return {"message": "Hello World!"}
