import sqlite3
from typing import Optional, Dict, Any
from datetime import datetime, timezone


class Database:
    def __init__(self, db_path: str = "url_shortener.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    short_code TEXT PRIMARY KEY,
                    target_url TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    expires_at TEXT,
                    click_count INTEGER DEFAULT 0,
                    last_accessed TEXT
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def save_url(
        self,
        short_code: str,
        target_url: str,
        created_at: datetime,
        expires_at: Optional[datetime],
    ) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO urls (short_code, target_url, created_at, expires_at, click_count)
                VALUES (?, ?, ?, ?, 0)
            """,
                (
                    short_code,
                    target_url,
                    created_at.isoformat(),
                    expires_at.isoformat() if expires_at else None,
                ),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_url(self, short_code: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM urls WHERE short_code = ?", (short_code,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            now = datetime.now(timezone.utc).isoformat()
            cursor.execute(
                """
                UPDATE urls 
                SET click_count = click_count + 1, last_accessed = ? 
                WHERE short_code = ?
            """,
                (now, short_code),
            )
            conn.commit()
            return dict(row)
        finally:
            conn.close()

    def get_analytics(self, short_code: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM urls WHERE short_code = ?", (short_code,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()


db = Database()