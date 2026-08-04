"""Agente Gemini per analizzare offerte di lavoro."""

import json

from google import genai
from pydantic import ValidationError

from candidate_profile import CANDIDATE_PROFILE
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    validate_settings,
)
from models import JobAnalysis


SYSTEM_INSTRUCTION = """
You are a strict and realistic job-search assistant for Switzerland.

You compare job advertisements with the candidate profile.

Rules:

1. Never invent experience, qualifications, projects or language levels.
2. The candidate completed a full-stack diploma but does not yet have
   commercial software-development experience.
3. Distinguish mandatory requirements from preferences.
4. Do not reject a position merely because one optional skill is missing.
5. Treat mandatory senior experience as a serious blocker.
6. Treat mandatory German C1 or native-level German as a possible blocker.
7. Treat German B2 as a meaningful gap, but not automatically a blocker.
8. Consider transferable skills from hospitality when relevant.
9. Consider developer, IT support, application support, technical support,
   QA, implementation and suitable technology-office roles.
10. Give a realistic score rather than an encouraging score.
11. Never guarantee an interview.
12. Return only information supported by the job advertisement and profile.
13. Write all explanations in Italian.
"""


class JobAnalyser:
    """Confronta un'offerta di lavoro con il profilo della candidata."""

    def __init__(self) -> None:
        validate_settings()

        self.client = genai.Client(
            api_key=GEMINI_API_KEY,
        )

    def analyse(
        self,
        job_description: str,
        provided_title: str = "",
        provided_company: str = "",
        job_url: str = "",
    ) -> JobAnalysis:
        """Analizza un annuncio e restituisce un JobAnalysis validato."""

        clean_description = job_description.strip()

        if len(clean_description) < 100:
            raise ValueError(
                "La descrizione è troppo breve. "
                "Incolla almeno 100 caratteri dell'annuncio."
            )

        prompt = self._build_prompt(
            job_description=clean_description,
            provided_title=provided_title.strip(),
            provided_company=provided_company.strip(),
            job_url=job_url.strip(),
        )

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "temperature": 0.2,
                "response_mime_type": "application/json",
                "response_schema": JobAnalysis,
            },
        )

        if not response.text:
            raise RuntimeError(
                "Gemini non ha restituito alcuna analisi."
            )

        try:
            return JobAnalysis.model_validate_json(
                response.text
            )

        except ValidationError as error:
            raise RuntimeError(
                "Gemini ha restituito un risultato "
                "che non rispetta il formato previsto."
            ) from error

    @staticmethod
    def _build_prompt(
        job_description: str,
        provided_title: str,
        provided_company: str,
        job_url: str,
    ) -> str:
        """Costruisce il testo inviato a Gemini."""

        profile_json = json.dumps(
            CANDIDATE_PROFILE,
            ensure_ascii=False,
            indent=2,
        )

        return f"""
Analyse this job opportunity for the candidate.

CANDIDATE PROFILE

{profile_json}

INFORMATION ENTERED BY THE USER

Job title:
{provided_title or "Not provided"}

Company:
{provided_company or "Not provided"}

Job URL:
{job_url or "Not provided"}

COMPLETE JOB ADVERTISEMENT

{job_description}

SCORING RULES

90-100:
Excellent match. The candidate satisfies nearly all important
requirements and has no major blocker.

75-89:
Good match. The candidate should normally apply.

60-74:
Possible match. Relevant gaps exist, but applying may still
be worthwhile.

40-59:
Weak match. Apply only for a clear strategic reason.

0-39:
Poor match or serious mandatory blockers.

Use the title and company entered by the user when they are
provided and consistent with the advertisement.

When information is absent, write Not specified.
Do not guess.
"""
