from fastapi import FastAPI
from fastapi.responses import Response


#Инициализация FastAPI проекта
app = FastAPI()


@app.get("/health")
def health_cheack():
    return Response(status_code=200)