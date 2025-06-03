from fastapi import FastAPI
from mediaflow_proxy.main import app as mediaflow_app   # Import the built‑in proxy app
import os

# 1) Create a new FastAPI instance that will “wrap” the proxy
main_app = FastAPI()

# 2) Register /status first, so it isn’t shadowed by the proxy’s “static at /” mount
@main_app.get("/status")
def status(apiPassword: str):
    if apiPassword == os.getenv("API_PASSWORD"):
        return {"status": "ok"}
    return {"status": "unauthorized"}

# 3) Now copy every route from mediaflow_app EXCEPT the “/” static‑files mount
for route in mediaflow_app.routes:
    if route.path != "/":    
        main_app.router.routes.append(route)

# 4) Run with uvicorn when you do “python run.py” locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=7860)
