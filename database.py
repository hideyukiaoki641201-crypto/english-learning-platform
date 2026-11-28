
# ① 必要なライブラリを読み込む
import sqlite3
from pathlib import Path


# ② データベースファイルの保存場所を指定する
DB_NAME = Path(__file__).resolve().parent / "vocabulary.db"


# ③ データベースに接続する共通関数
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ④ データベースのテーブルを初期化する
def initialize_database():
    conn = get_connection()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                sense_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                meaning TEXT NOT NULL,
                expression_key TEXT NOT NULL,
                meaning_key TEXT NOT NULL,
                UNIQUE(expression_key, meaning_key)
            )
        """)

        conn.commit()

    finally:
        conn.close()

