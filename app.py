import plotly.express as px
import streamlit as st

from src.ai_analyst import ask

st.set_page_config(page_title="AI Data Job Market Analyst", page_icon="📊", layout="wide")

st.title("📊 AI Data Job Market Analyst")
st.caption(
    "Ask a plain-English question about the data job market. "
    "Claude writes the SQL, runs it live against the database, and explains the results."
)

SAMPLE_QUESTIONS = [
    "What are the top 10 highest paying Data Analyst jobs that allow remote work?",
    "What are the 5 most in-demand skills for Data Analysts?",
    "Which skills have the highest average salary for remote Data Analyst roles?",
    "How many job postings mention no degree required, by job title?",
]

with st.sidebar:
    st.subheader("Try a sample question")
    for q in SAMPLE_QUESTIONS:
        if st.button(q, use_container_width=True):
            st.session_state["question"] = q
    st.divider()
    st.caption(
        "This app only ever runs SELECT queries — the AI-generated SQL "
        "is shown below so you can verify exactly what ran."
    )

question = st.text_input(
    "Ask a question about the job market",
    value=st.session_state.get("question", ""),
    placeholder="e.g. What skills pay the most for remote data analyst jobs?",
)

if st.button("Ask", type="primary") and question:
    with st.spinner("Claude is writing SQL and querying the database..."):
        try:
            sql, df, summary = ask(question)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            st.subheader("Results")
            st.dataframe(df, use_container_width=True)

            numeric_cols = df.select_dtypes(include="number").columns
            label_cols = df.select_dtypes(exclude="number").columns
            if len(df) > 1 and len(numeric_cols) > 0 and len(label_cols) > 0:
                fig = px.bar(df, x=label_cols[0], y=numeric_cols[0])
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("AI Insight")
            st.info(summary)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
