from fastapi import FastAPI
from mediaflow_proxy.main import app as mediaflow_app
import os

main_app = FastAPI()

@main_app.get("/status")
def status(apiPassword: str):
    """Liveness check: returns {"status":"ok"} if the query‐param matches."""
    if apiPassword == os.getenv("API_PASSWORD"):
        return {"status": "ok"}
    return {"status": "unauthorized"}

# Append all mediaflow routes except "/" and "/status"
for route in mediaflow_app.routes:
    if route.path not in ["/", "/status"]:
        main_app.router.routes.append(route)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=7860)
