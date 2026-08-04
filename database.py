"""Gestione del database SQLite del Job AI Agent."""

import json
import sqlite3
from datetime import datetime
from typing import Any

from config import DATABASE_PATH
from models import JobAnalysis


VALID_STATUSES = [
    "Nuova",
    "Da valutare",
    "Da candidare",
    "Candidatura inviata",
    "Colloquio",
    "Rifiutata",
    "Offerta ricevuta",
    "Archiviata",
]


def get_connection() -> sqlite3.Connection:
    """Apre una connessione al database SQLite."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialise_database() -> None:
    """Crea la tabella delle offerte se non esiste."""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                job_url TEXT,
                job_description TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                recommendation TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Nuova',
                analysis_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                applied_at TEXT,
                notes TEXT
            )
            """
        )

        connection.commit()


def save_job(
    analysis: JobAnalysis,
    job_description: str,
    job_url: str = "",
) -> int:
    """Salva un'offerta e restituisce il suo ID."""

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO jobs (
                job_title,
                company,
                location,
                job_url,
                job_description,
                match_score,
                recommendation,
                status,
                analysis_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                analysis.job_title,
                analysis.company,
                analysis.location,
                job_url.strip(),
                job_description.strip(),
                analysis.match_score,
                analysis.recommendation,
                "Nuova",
                analysis.model_dump_json(),
                created_at,
            ),
        )

        connection.commit()

        if cursor.lastrowid is None:
            raise RuntimeError(
                "Il database non ha restituito l'ID."
            )

        return int(cursor.lastrowid)


def get_all_jobs() -> list[dict[str, Any]]:
    """Restituisce tutte le offerte salvate."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                job_title,
                company,
                location,
                job_url,
                match_score,
                recommendation,
                status,
                created_at
            FROM jobs
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def get_job(job_id: int) -> dict[str, Any] | None:
    """Restituisce tutti i dati di una singola offerta."""

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM jobs
            WHERE id = ?
            """,
            (job_id,),
        ).fetchone()

    if row is None:
        return None

    result = dict(row)

    result["analysis"] = json.loads(
        result["analysis_json"]
    )

    return result


def update_job_status(
    job_id: int,
    status: str,
) -> None:
    """Aggiorna lo stato della candidatura."""

    if status not in VALID_STATUSES:
        raise ValueError(
            "Stato della candidatura non valido."
        )

    with get_connection() as connection:
        if status == "Candidatura inviata":
            applied_at = datetime.now().isoformat(
                timespec="seconds"
            )

            connection.execute(
                """
                UPDATE jobs
                SET status = ?, applied_at = ?
                WHERE id = ?
                """,
                (
                    status,
                    applied_at,
                    job_id,
                ),
            )

        else:
            connection.execute(
                """
                UPDATE jobs
                SET status = ?
                WHERE id = ?
                """,
                (
                    status,
                    job_id,
                ),
            )

        connection.commit()


def update_job_notes(
    job_id: int,
    notes: str,
) -> None:
    """Aggiorna le note di una candidatura."""

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE jobs
            SET notes = ?
            WHERE id = ?
            """,
            (
                notes.strip(),
                job_id,
            ),
        )

        connection.commit()


def delete_job(job_id: int) -> None:
    """Elimina un'offerta."""

    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM jobs
            WHERE id = ?
            """,
            (job_id,),
        )

        connection.commit()
