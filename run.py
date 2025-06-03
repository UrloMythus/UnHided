from fastapi import FastAPI
from mediaflow_proxy.main import app as mediaflow_app  # Import the original MediaFlow proxy app
import os

# 1) Create a brand‐new FastAPI instance for our merged app
main_app = FastAPI()

# 2) Define /status *before* we attach the mediaflow routes
@main_app.get("/status")
def status(apiPassword: str):
    """
    Liveness check: returns {"status":"ok"} if the query‐param apiPassword
    matches the API_PASSWORD environment variable.
    """
    if apiPassword == os.getenv("API_PASSWORD"):
        return {"status": "ok"}
    return {"status": "unauthorized"}

# 3) Now append all of mediaflow_app’s routes, EXCEPT:
#    • '/' (the static‐files catch‐all)
#    • '/status' (so that our status isn’t overwritten)
for route in mediaflow_app.routes:
    if route.path not in ["/", "/status"]:
        main_app.router.routes.append(route)


# 4) Finally, if someone runs this file directly, start Uvicorn on 7860
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(main_app, host="0.0.0.0", port=7860)
