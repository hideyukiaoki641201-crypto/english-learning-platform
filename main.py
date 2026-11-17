
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "English Learning Platform is running!"}

@app.get("/vocabulary")
def get_vocabulary():
    return [
        {"expression": "take over", "meaning": "引き継ぐ"},
        {"expression": "follow up", "meaning": "追加で確認する"}
    ]





