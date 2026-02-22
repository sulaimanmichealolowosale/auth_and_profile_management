from fastapi import FastAPI
from app.routes.auth import auth_controller
from app.routes.profile import profile_controller


app = FastAPI()
class Route:
    def __init__(self, *args) -> None:
        [app.include_router(keys.router) for keys in args]


app_route = Route(
    auth_controller,
    profile_controller
    )


@app.get('/')
def main():
    return {"message":"You are welcome"}

# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload