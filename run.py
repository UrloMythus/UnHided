from fastapi import FastAPI
from mediaflow_proxy.main import app as mediaflow_app  # Import mediaflow app
import httpx
import re
import string
import os

# Initialize the main FastAPI application
main_app = FastAPI()

# Add all routes from mediaflow_app except "/", "/status" to avoid conflicts
for route in mediaflow_app.routes:
    if route.path not in ["/status"]:
        main_app.router.routes.append(route)

# Add /status route for API liveness check
@main_app.get("/status")
def status(apiPassword: str):
    if apiPassword == os.getenv("API_PASSWORD"):
        return {"status": "ok"}
    return {"status": "unauthorized"}

# Run the main app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=7860)
