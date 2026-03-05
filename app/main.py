from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings
from app.database.database import engine, Base
from app.api import health, routes

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title=settings.PROJECT_NAME)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        routes=app.routes,
    )
    # Patch for Swagger UI: OpenAPI 3.1 file uploads show as string without 'format: binary'
    if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
        for schema_name, schema_data in openapi_schema["components"]["schemas"].items():
            if "properties" in schema_data:
                for prop_name, prop_data in schema_data["properties"].items():
                    if prop_data.get("type") == "string" and prop_data.get("contentMediaType") == "application/octet-stream":
                        prop_data["format"] = "binary"
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(routes.router, tags=["Tumor Detection API"])

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

