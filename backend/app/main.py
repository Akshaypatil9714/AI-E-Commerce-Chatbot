from fastapi import FastAPI
from app.api import router as chat_router

app = FastAPI()

app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug = True)
