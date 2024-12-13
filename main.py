from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from markers import router as markers_router
from fastapi.responses import JSONResponse
from fastapi import Request

app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the exception details (optional)
    print(f"Unhandled exception: {exc}")

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


# CORS Configuration
origins = [
    "<https://eventual-frontend.vercel.app>",  # Replace with your actual frontend URL
    "<http://localhost:5173>",  # For local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers after adding middleware
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(markers_router, prefix="/markers", tags=["Markers"])
