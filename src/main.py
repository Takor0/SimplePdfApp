from fastapi import FastAPI

from endpoints import file
app = FastAPI()
app.include_router(file.router)