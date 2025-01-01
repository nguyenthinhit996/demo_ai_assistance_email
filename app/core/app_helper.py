from fastapi import FastAPI

# Placeholder for the app instance
_app: FastAPI = None

def set_app(app: FastAPI):
    global _app
    _app = app

def get_app() -> FastAPI:
    global _app
    if _app is None:
        raise RuntimeError("App is not set. Ensure `set_app` is called during initialization.")
    return _app
