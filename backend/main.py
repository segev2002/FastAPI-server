import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from db import init_db, save_log
from routes import router

init_db()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

# Rate limit: each IP address can send up to 100 requests per hour
app.state.limiter = Limiter(key_func=get_remote_address, application_limits=["100/hour"])
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


# Runs on every request: measures the time and saves a row in the logs table
@app.middleware("http")
async def log_request(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000, 2)
    save_log(f"Status {response.status_code}", request.method, str(request.url.path), duration_ms)
    return response
