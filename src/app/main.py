from fastapi import FastAPI
from engine import engine
app = FastAPI()


@app.get("/")
def root():
    return "No response"


@app.get("/{query}")
def read_item(query: str):
    return engine.ask(query)
