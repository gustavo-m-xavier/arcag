from fastapi import FastAPI

from .routes.graph import router as graph_router
from .routes.health import router as health_router


app = FastAPI(
    title="ARCAG Citation Graph API",
    description="Search scientific papers and explore their citation relationships.",
    version="1.0.0",
)
app.include_router(health_router)
app.include_router(graph_router)
