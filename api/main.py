from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

DATABASE = "coordinates.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
async def root():
    return {"message": "Welcome to the CTF SQL Injection challenge!"}


@app.get("/points")
async def get_points(query: str):
    """
    WARNING: This endpoint is intentionally vulnerable to SQL Injection
    for CTF purposes.
    Example: /points?query=1 OR 1=1
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vulnerable query (for CTF practice)
    sql = f"SELECT * FROM points WHERE id = {query};"
    print("Executing:", sql)

    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    return {"results": [dict(row) for row in rows]}
