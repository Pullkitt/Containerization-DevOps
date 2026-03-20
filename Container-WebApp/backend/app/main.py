import os
import time
from contextlib import contextmanager

import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr


app = FastAPI(title="Container WebApp API", version="1.0.0")


DB_HOST = os.getenv("DB_HOST", "database")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")


class RecordCreate(BaseModel):
    name: str
    email: EmailStr


def db_connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@contextmanager
def get_cursor():
    conn = db_connect()
    try:
        cur = conn.cursor()
        yield conn, cur
    finally:
        conn.close()


def init_db_with_retry(max_attempts: int = 30, delay_seconds: int = 2) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            with get_cursor() as (conn, cur):
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS records (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                )
                conn.commit()
            return
        except Exception:
            if attempt == max_attempts:
                raise
            time.sleep(delay_seconds)


@app.on_event("startup")
def startup_event() -> None:
    init_db_with_retry()


@app.get("/health")
def healthcheck():
    try:
        with get_cursor() as (_, cur):
            cur.execute("SELECT 1;")
            cur.fetchone()
        return {"status": "ok", "database": "reachable"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Database unreachable: {exc}") from exc


@app.post("/records", status_code=201)
def create_record(payload: RecordCreate):
    try:
        with get_cursor() as (conn, cur):
            cur.execute(
                """
                INSERT INTO records (name, email)
                VALUES (%s, %s)
                RETURNING id, name, email, created_at;
                """,
                (payload.name, payload.email),
            )
            inserted = cur.fetchone()
            conn.commit()
        return {
            "id": inserted[0],
            "name": inserted[1],
            "email": inserted[2],
            "created_at": str(inserted[3]),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to insert record: {exc}") from exc


@app.get("/records")
def list_records():
    try:
        with get_cursor() as (_, cur):
            cur.execute(
                """
                SELECT id, name, email, created_at
                FROM records
                ORDER BY id;
                """
            )
            rows = cur.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "created_at": str(row[3]),
            }
            for row in rows
        ]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch records: {exc}") from exc
