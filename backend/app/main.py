from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import identities, paths, risk, guard

app = FastAPI(
    title="PrivilegePredict API",
    description="API for multi-cloud identity graph and privilege escalation analysis",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(identities.router, prefix="/identities", tags=["identities"])
app.include_router(paths.router, prefix="/paths", tags=["paths"])
app.include_router(risk.router, prefix="/risk", tags=["risk"])
app.include_router(guard.router, prefix="/guard", tags=["guard"])

@app.get("/")
async def root():
    return {"message": "Welcome to PrivilegePredict API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}