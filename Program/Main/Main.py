from fastapi import FastAPI
from Routes.Routes import router

app = FastAPI()

# Підключення маршрутів
app.include_router(router)