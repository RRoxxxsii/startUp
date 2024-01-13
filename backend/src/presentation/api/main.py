import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/hello/')
def greeting():
    return {"message": "Hello world from FastAPI!"}


if __name__ == "__main__":
    uvicorn.run(
        app="src.presentation.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
