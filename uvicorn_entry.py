import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT") or 8000), reload=True)