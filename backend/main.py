import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from db import init_db, save_log
from routes import router

init_db()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)


# Runs on every request: measures the time and saves a row in the logs table
@app.middleware("http")
async def log_request(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000, 2)
    save_log(f"Status {response.status_code}", request.method, str(request.url.path), duration_ms)
    return response
