import uvicorn
import sys
from os import path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routes import router
parent_dir = path.dirname(path.dirname(__file__))
sys.path.insert(0, parent_dir)



api = FastAPI()
@api.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")


def main():
    configure()
    uvicorn.run(
        app=api,
        host="localhost",
        port=8000,
    )


def configure():
    # configure_db()
    configure_routes()
    configure_middleware()

def configure_routes():
    api.router.prefix = "/api"
    api.include_router(router, prefix="/estimate")


def configure_middleware():
    origins = [
        "http://localhost:1420",
    ]
    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    main()
else:
    configure()
   
