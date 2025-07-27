from fastapi import FastAPI
from app.routes.user_routes import router as user_router
import uvicorn
import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/user.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize FastAPI app
app = FastAPI()

# Include user routes
app.include_router(user_router)

# Health check
@app.get("/")
def read_root():
    return {"message": "User Registration API is running"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
