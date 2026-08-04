"""Configurazione generale del Job AI Agent."""

import os
from pathlib import Path

from dotenv import load_dotenv


# Cartella principale del progetto.
BASE_DIR = Path(__file__).resolve().parent

# Carica le variabili presenti nel file .env.
load_dotenv(BASE_DIR / ".env")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash",
)

DATABASE_PATH = BASE_DIR / "data" / "jobs.db"


def validate_settings() -> None:
    """Controlla che le configurazioni necessarie siano presenti."""

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY non trovata. "
            "Controlla il file .env."
        )

    if not GEMINI_MODEL:
        raise RuntimeError(
            "GEMINI_MODEL non configurato."
        )
