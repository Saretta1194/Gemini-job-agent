"""Modelli Pydantic per i risultati prodotti da Gemini."""

from typing import Literal

from pydantic import BaseModel, Field


class JobAnalysis(BaseModel):
    """Risultato strutturato dell'analisi di un'offerta."""

    job_title: str = Field(
        description=(
            "Titolo della posizione. Usa Unknown se non è disponibile."
        )
    )

    company: str = Field(
        description=(
            "Nome dell'azienda. Usa Unknown se non è disponibile."
        )
    )

    location: str = Field(
        description=(
            "Località della posizione. Usa Not specified se assente."
        )
    )

    employment_percentage: str = Field(
        description=(
            "Percentuale lavorativa oppure Not specified."
        )
    )

    schedule: str = Field(
        description=(
            "Giorni, turni e orari indicati oppure Not specified."
        )
    )

    salary: str = Field(
        description=(
            "Salario indicato nell'annuncio oppure Not specified."
        )
    )

    match_score: int = Field(
        ge=0,
        le=100,
        description="Compatibilità realistica da 0 a 100.",
    )

    recommendation: Literal[
        "strong_apply",
        "apply",
        "consider",
        "skip",
    ] = Field(
        description="Decisione consigliata."
    )

    matched_requirements: list[str] = Field(
        description=(
            "Requisiti importanti già soddisfatti dalla candidata."
        )
    )

    missing_requirements: list[str] = Field(
        description=(
            "Requisiti presenti nell'annuncio ma assenti dal profilo."
        )
    )

    hard_blockers: list[str] = Field(
        description=(
            "Problemi che potrebbero impedire realmente la candidatura."
        )
    )

    transferable_strengths: list[str] = Field(
        description=(
            "Competenze trasferibili dalla carriera nella ristorazione."
        )
    )

    relevant_projects: list[str] = Field(
        description=(
            "Progetti portfolio pertinenti per questa posizione."
        )
    )

    main_risks: list[str] = Field(
        description=(
            "Principali debolezze o rischi della candidatura."
        )
    )

    reason: str = Field(
        description=(
            "Spiegazione concreta e onesta della valutazione."
        )
    )

    next_action: str = Field(
        description=(
            "Prossimo passo pratico consigliato alla candidata."
        )
    )
