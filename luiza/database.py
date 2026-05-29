import sqlite3
from contextlib import contextmanager

DB_PATH = "hotel_lumina.db"


def init_db():
    with _conn() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS bookings (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id          INTEGER NOT NULL,
                room_name        TEXT    NOT NULL,
                guest_name       TEXT    NOT NULL,
                guest_email      TEXT    NOT NULL,
                guest_phone      TEXT    DEFAULT '',
                check_in         TEXT    NOT NULL,
                check_out        TEXT    NOT NULL,
                num_guests       INTEGER NOT NULL DEFAULT 1,
                nights           INTEGER NOT NULL,
                total_price      REAL    NOT NULL,
                special_requests TEXT    DEFAULT '',
                status           TEXT    DEFAULT 'confirmed',
                created_at       TEXT    DEFAULT (datetime('now','localtime'))
            );
        """)


@contextmanager
def _conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def get_occupied_ranges(room_id: int) -> list[dict]:
    with _conn() as db:
        rows = db.execute(
            "SELECT check_in, check_out FROM bookings "
            "WHERE room_id = ? AND status != 'cancelled'",
            (room_id,)
        ).fetchall()
    return [{"from": r["check_in"], "to": r["check_out"]} for r in rows]


def is_available(room_id: int, check_in: str, check_out: str) -> bool:
    """True dacă nicio rezervare existentă nu se suprapune cu intervalul dat."""
    with _conn() as db:
        row = db.execute("""
            SELECT COUNT(*) AS cnt FROM bookings
            WHERE room_id = ?
              AND status  != 'cancelled'
              AND check_in  < ?
              AND check_out > ?
        """, (room_id, check_out, check_in)).fetchone()
    return row["cnt"] == 0


def create_booking(data: dict) -> int:
    with _conn() as db:
        cur = db.execute("""
            INSERT INTO bookings
                (room_id, room_name, guest_name, guest_email, guest_phone,
                 check_in, check_out, num_guests, nights, total_price, special_requests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["room_id"],       data["room_name"],
            data["guest_name"],    data["guest_email"],   data.get("guest_phone", ""),
            data["check_in"],      data["check_out"],
            data["num_guests"],    data["nights"],
            data["total_price"],   data.get("special_requests", ""),
        ))
        return cur.lastrowid


def get_all_bookings() -> list:
    with _conn() as db:
        return db.execute(
            "SELECT * FROM bookings ORDER BY created_at DESC"
        ).fetchall()
