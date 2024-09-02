from fastapi import FastAPI
from app.api import router as chat_router
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse 

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://ai-e-commerce-chatbot.vercel.app",
    #         "http://localhost:8080",
    # ],  # Update this with your Vercel domain or "*" to allow all origins
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(chat_router)

# Serve the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a simple root endpoint to avoid 404 at "/"
@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI E-Commerce Chatbot API!"}

# Serve the favicon.ico directly at the root path
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
