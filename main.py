
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "English Learning Platform is running!"}

@app.get("/vocabulary")
def get_vocabulary(search: str = ""):
    if not search:
        return vocabulary_items

    return [
        item for item in vocabulary_items
        if search.casefold() in item["expression"].casefold()
    ]
from pydantic import BaseModel

# 登録する単語のデータ形式
class VocabularyItem(BaseModel):
    expression: str
    meaning: str

# 一時的に単語を保存するリスト
vocabulary_items = []

@app.post("/vocabulary")
def add_vocabulary(item: VocabularyItem):
    for existing in vocabulary_items:
        if (
            existing["expression"].strip().casefold() == item.expression.strip().casefold()
            and existing["meaning"].strip() == item.meaning.strip()
        ):
            return {
                "message": "Vocabulary already exists",
                "item": existing
            }

    vocabulary_items.append(item.model_dump())
    return {
        "message": "Vocabulary registered successfully",
        "item": item
    }





