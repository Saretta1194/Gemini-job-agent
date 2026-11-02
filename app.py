
"""Public, read-only Streamlit portfolio demo of the Job AI Agent."""

import streamlit as st

from demo_data import DEMO_DESCRIPTION, get_demo_analysis
from models import JobAnalysis

st.set_page_config(
    page_title="Job AI Agent | Portfolio Demo",
    page_icon="💼",
    layout="wide",
)

RECOMMENDATION_LABELS = {
    "strong_apply": "Highly recommended",
    "apply": "Recommended",
    "consider": "Consider carefully",
    "skip": "Not recommended",
}

RECOMMENDATION_ICONS = {
    "strong_apply": "✅",
    "apply": "👍",
    "consider": "⚠️",
    "skip": "❌",
}


def display_list(
    title: str,
    items: list[str],
    empty_message: str = "None identified.",
) -> None:
    st.subheader(title)
    if items:
        for item in items:
            st.markdown(f"- {item}")
    else:
        st.write(empty_message)


def display_analysis(analysis: JobAnalysis) -> None:
    st.divider()
    st.header(analysis.job_title)
    st.caption(
        "Sample result · Fictional job posting · No live AI processing"
    )

    st.markdown(
        f"**Company:** {analysis.company}  \n"
        f"**Location:** {analysis.location}  \n"
        f"**Employment:** {analysis.employment_percentage}  \n"
        f"**Schedule:** {analysis.schedule}  \n"
        f"**Salary:** {analysis.salary}"
    )

    score_column, recommendation_column = st.columns(2)

    with score_column:
        st.metric(
            "Illustrative match score",
            f"{analysis.match_score}%",
        )
        st.progress(analysis.match_score / 100)

    with recommendation_column:
        label = RECOMMENDATION_LABELS.get(
            analysis.recommendation,
            analysis.recommendation,
        )
        icon = RECOMMENDATION_ICONS.get(
            analysis.recommendation,
            "ℹ️",
        )
        st.metric(
            "Sample recommendation",
            f"{icon} {label}",
        )

    st.info(analysis.reason)

    left_column, right_column = st.columns(2)

    with left_column:
        display_list(
            "Matching requirements",
            analysis.matched_requirements,
        )
        display_list(
            "Relevant projects",
            analysis.relevant_projects,
        )
        display_list(
            "Transferable strengths",
            analysis.transferable_strengths,
        )

    with right_column:
        display_list(
            "Missing requirements",
            analysis.missing_requirements,
        )
        display_list(
            "Potential blockers",
            analysis.hard_blockers,
        )
        display_list(
            "Main risks",
            analysis.main_risks,
        )

    st.success(
        f"Suggested next step: {analysis.next_action}"
    )


st.title("💼 Job AI Agent")

st.write(
    "A portfolio project exploring how generative AI can compare "
    "job requirements with a candidate's technical skills and experience."
)

st.info(
    "**Public demo mode:** This page displays a predefined example. "
    "It does not call the Gemini API, analyse new job postings, "
    "or store visitor information."
)

with st.expander("View fictional job description"):
    st.text(DEMO_DESCRIPTION)

if st.button(
    "▶ Try Demo",
    type="primary",
    use_container_width=True,
):
    st.session_state.show_demo = True

if st.session_state.get("show_demo", False):
    display_analysis(get_demo_analysis())

st.divider()

st.caption(
    "Built with Python, Streamlit, Pydantic and the Google Gemini SDK. "
    "The live AI feature is disabled in this public demonstration."
)
