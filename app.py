"""Interfaccia Streamlit del Job AI Agent."""

import streamlit as st

from agents.job_analyser import JobAnalyser
from candidate_profile import CANDIDATE_PROFILE
from database import (
    VALID_STATUSES,
    delete_job,
    get_all_jobs,
    get_job,
    initialise_database,
    save_job,
    update_job_notes,
    update_job_status,
)
from models import JobAnalysis


st.set_page_config(
    page_title="Sara's Job Agent",
    page_icon="💼",
    layout="wide",
)


initialise_database()


RECOMMENDATION_LABELS = {
    "strong_apply": "Candidati assolutamente",
    "apply": "Candidati",
    "consider": "Valuta con attenzione",
    "skip": "Lascia perdere",
}

RECOMMENDATION_ICONS = {
    "strong_apply": "✅",
    "apply": "👍",
    "consider": "⚠️",
    "skip": "❌",
}


if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None

if "current_description" not in st.session_state:
    st.session_state.current_description = ""

if "current_url" not in st.session_state:
    st.session_state.current_url = ""

if "current_analysis_saved" not in st.session_state:
    st.session_state.current_analysis_saved = False


def display_list(
    title: str,
    items: list[str],
    empty_message: str = "Nessuna informazione.",
) -> None:
    """Visualizza una lista in modo leggibile."""

    st.subheader(title)

    if not items:
        st.write(empty_message)
        return

    for item in items:
        st.markdown(f"- {item}")


def display_analysis(
    analysis: JobAnalysis,
) -> None:
    """Mostra il risultato dell'analisi."""

    recommendation_label = RECOMMENDATION_LABELS.get(
        analysis.recommendation,
        analysis.recommendation,
    )

    recommendation_icon = RECOMMENDATION_ICONS.get(
        analysis.recommendation,
        "ℹ️",
    )

    st.divider()

    st.header(analysis.job_title)

    st.markdown(
        f"""
**Azienda:** {analysis.company}
**Località:** {analysis.location}
**Percentuale:** {analysis.employment_percentage}
**Orari:** {analysis.schedule}
**Salario:** {analysis.salary}
"""
    )

    score_column, recommendation_column = st.columns(2)

    with score_column:
        st.metric(
            "Compatibilità",
            f"{analysis.match_score}%",
        )

        st.progress(
            analysis.match_score / 100
        )

    with recommendation_column:
        st.metric(
            "Decisione",
            (
                f"{recommendation_icon} "
                f"{recommendation_label}"
            ),
        )

    st.info(analysis.reason)

    left_column, right_column = st.columns(2)

    with left_column:
        display_list(
            "Requisiti compatibili",
            analysis.matched_requirements,
        )

        display_list(
            "Progetti pertinenti",
            analysis.relevant_projects,
        )

        display_list(
            "Competenze trasferibili",
            analysis.transferable_strengths,
        )

    with right_column:
        display_list(
            "Requisiti mancanti",
            analysis.missing_requirements,
        )

        display_list(
            "Ostacoli reali",
            analysis.hard_blockers,
            "Nessun ostacolo certo identificato.",
        )

        display_list(
            "Rischi principali",
            analysis.main_risks,
        )

    st.success(
        f"Prossimo passo: {analysis.next_action}"
    )


def analyse_page() -> None:
    """Pagina per analizzare un'offerta."""

    st.title("💼 Job AI Agent")

    st.write(
        "Incolla un'offerta di lavoro. "
        "Gemini la confronterà con il tuo profilo reale."
    )

    with st.form("analysis_form"):
        title = st.text_input(
            "Titolo della posizione",
            placeholder="Junior Python Developer",
        )

        company = st.text_input(
            "Azienda",
            placeholder="Example AG",
        )

        job_url = st.text_input(
            "Link dell'offerta",
            placeholder="https://...",
        )

        description = st.text_area(
            "Descrizione completa dell'offerta",
            height=350,
            placeholder=(
                "Incolla qui responsabilità, requisiti, "
                "lingue, luogo, salario e percentuale..."
            ),
        )

        submitted = st.form_submit_button(
            "Analizza offerta",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        st.session_state.current_analysis_saved = False

        if len(description.strip()) < 100:
            st.error(
                "La descrizione è troppo breve. "
                "Incolla almeno 100 caratteri."
            )

        else:
            try:
                with st.spinner(
                    "Gemini sta analizzando l'offerta..."
                ):
                    analyser = JobAnalyser()

                    result = analyser.analyse(
                        job_description=description,
                        provided_title=title,
                        provided_company=company,
                        job_url=job_url,
                    )

                st.session_state.current_analysis = result
                st.session_state.current_description = description
                st.session_state.current_url = job_url

            except Exception as error:
                st.error(
                    "Non è stato possibile analizzare l'offerta."
                )

                with st.expander("Dettagli tecnici"):
                    st.exception(error)

    analysis = st.session_state.current_analysis

    if analysis is not None:
        display_analysis(analysis)

        if st.session_state.current_analysis_saved:
            st.success(
                "Questa offerta è già stata salvata."
            )

        else:
            if st.button(
                "Salva offerta",
                type="primary",
                use_container_width=True,
            ):
                try:
                    job_id = save_job(
                        analysis=analysis,
                        job_description=(
                            st.session_state.current_description
                        ),
                        job_url=(
                            st.session_state.current_url
                        ),
                    )

                    st.session_state.current_analysis_saved = True

                    st.success(
                        f"Offerta salvata con ID {job_id}."
                    )

                except Exception as error:
                    st.error(
                        "Non è stato possibile salvare l'offerta."
                    )

                    with st.expander("Dettagli tecnici"):
                        st.exception(error)


def applications_page() -> None:
    """Pagina delle candidature salvate."""

    st.title("📋 Candidature")

    jobs = get_all_jobs()

    if not jobs:
        st.info(
            "Non hai ancora salvato offerte."
        )
        return

    st.write(
        f"Offerte salvate: **{len(jobs)}**"
    )

    for job in jobs:
        expander_title = (
            f"{job['job_title']} — "
            f"{job['company']} — "
            f"{job['match_score']}%"
        )

        with st.expander(expander_title):
            details = get_job(job["id"])

            if details is None:
                st.warning(
                    "Non è stato possibile leggere l'offerta."
                )
                continue

            analysis = details["analysis"]

            st.markdown(
                f"""
**Località:** {job['location']}
**Stato:** {job['status']}
**Salvata il:** {job['created_at']}
**Decisione AI:** {
    RECOMMENDATION_LABELS.get(
        job['recommendation'],
        job['recommendation'],
    )
}
"""
            )

            if job["job_url"]:
                st.markdown(
                    f"**Link:** {job['job_url']}"
                )

            st.write(
                f"**Motivazione:** {analysis['reason']}"
            )

            st.write(
                f"**Prossima azione:** {analysis['next_action']}"
            )

            status_column, notes_column = st.columns(2)

            with status_column:
                current_status = job["status"]

                try:
                    status_index = VALID_STATUSES.index(
                        current_status
                    )
                except ValueError:
                    status_index = 0

                selected_status = st.selectbox(
                    "Stato candidatura",
                    VALID_STATUSES,
                    index=status_index,
                    key=f"status_{job['id']}",
                )

                if st.button(
                    "Aggiorna stato",
                    key=f"update_status_{job['id']}",
                ):
                    update_job_status(
                        job_id=job["id"],
                        status=selected_status,
                    )

                    st.success(
                        "Stato aggiornato."
                    )

                    st.rerun()

            with notes_column:
                notes = st.text_area(
                    "Note",
                    value=details["notes"] or "",
                    key=f"notes_{job['id']}",
                    placeholder=(
                        "Contatto recruiter, scadenza, "
                        "documenti inviati..."
                    ),
                )

                if st.button(
                    "Salva note",
                    key=f"save_notes_{job['id']}",
                ):
                    update_job_notes(
                        job_id=job["id"],
                        notes=notes,
                    )

                    st.success(
                        "Note salvate."
                    )

            st.divider()

            if st.button(
                "Elimina offerta",
                key=f"delete_{job['id']}",
            ):
                delete_job(job["id"])

                st.success(
                    "Offerta eliminata."
                )

                st.rerun()


def profile_page() -> None:
    """Mostra il profilo utilizzato dall'agente."""

    st.title("👤 Profilo candidato")

    st.write(
        "Gemini usa questi dati per valutare le offerte."
    )

    st.json(CANDIDATE_PROFILE)


page = st.sidebar.radio(
    "Navigazione",
    [
        "Analizza offerta",
        "Candidature",
        "Profilo",
    ],
)

st.sidebar.divider()

st.sidebar.caption(
    "Il punteggio AI è orientativo e non garantisce "
    "un colloquio o un'assunzione."
)


if page == "Analizza offerta":
    analyse_page()

elif page == "Candidature":
    applications_page()

else:
    profile_page()
