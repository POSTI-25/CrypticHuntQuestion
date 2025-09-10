from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DATABASE = "coordinates.db"

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class RetrieveRequest(BaseModel):
    x_coordinate: str
    y_coordinate: str
    access_code: str

@app.post("/api/retrieve")
async def retrieve_data(req: RetrieveRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Intentionally vulnerable query (string interpolation, no sanitization)
        sql = f"""
        SELECT * FROM points
        WHERE x_coordinate = '{req.x_coordinate}'
          AND y_coordinate = '{req.y_coordinate}'
          AND flag = '{req.access_code}';
        """
        print("Executing:", sql)

        cursor.execute(sql)
        rows = cursor.fetchall()

        if rows:
            # If injection works, return ALL rows (including x,y,flag)
            results = []
            for row in rows:
                results.append({
                    "x_coordinate": row["x_coordinate"],
                    "y_coordinate": row["y_coordinate"],
                    "flag": row["flag"]
                })
            return {"status": "success", "data": {"payload": results}}
        else:
            return {
                "status": "error",
                "message": "Access Denied: Please Try Again"
            }

    except sqlite3.Error as e:
        return {"status": "error", "message": str(e)}

    finally:
        conn.close()
