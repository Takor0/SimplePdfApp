from fastapi import FastAPI


def create_app() -> FastAPI:
    from src.endpoints import file, task

    app = FastAPI()

    app.include_router(file.router)
    app.include_router(task.router)

    return app


app = create_app()
