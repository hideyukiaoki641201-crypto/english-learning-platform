# ① 必要なライブラリを読み込む
from fastapi import FastAPI
from pydantic import BaseModel

# ② 共通DBモジュールから関数を読み込む
from database import get_connection, initialize_database

# ③ FastAPIアプリを作成する
app = FastAPI()

# ④ データベースを初期化する
initialize_database()


# 登録する語彙のデータ形式
class VocabularyItem(BaseModel):
    expression: str
    meaning: str


@app.get("/")
def home():
    return {"message": "English Learning Platform is running!"}


# 登録済み語彙の取得・検索
@app.get("/vocabulary")
def get_vocabulary(search: str = ""):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT sense_ID, expression, meaning
            FROM vocabulary
            ORDER BY sense_ID
            """
        ).fetchall()

    return [
        dict(row)
        for row in rows
        if search.casefold() in row["expression"].casefold()
    ]


# 語彙の新規登録
@app.post("/vocabulary")
def add_vocabulary(item: VocabularyItem):
    expression = item.expression.strip()
    meaning = item.meaning.strip()

    if not expression or not meaning:
        return {"message": "Expression and meaning are required"}

    expression_key = expression.casefold()
    meaning_key = meaning

    with get_connection() as conn:
        existing = conn.execute(
            """
            SELECT sense_ID, expression, meaning
            FROM vocabulary
            WHERE expression_key = ? AND meaning_key = ?
            """,
            (expression_key, meaning_key)
        ).fetchone()

        if existing:
            return {
                "message": "Vocabulary already exists",
                "item": dict(existing)
            }

        cursor = conn.execute(
            """
            INSERT INTO vocabulary
                (expression, meaning, expression_key, meaning_key)
            VALUES (?, ?, ?, ?)
            """,
            (expression, meaning, expression_key, meaning_key)
        )

        return {
            "message": "Vocabulary registered successfully",
            "item": {
                "sense_ID": cursor.lastrowid,
                "expression": expression,
                "meaning": meaning
            }
        }
