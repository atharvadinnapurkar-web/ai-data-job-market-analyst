import os
from openai import OpenAI
from dotenv import load_dotenv
from .db import run_readonly_query

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "openrouter/free"  # auto-picks a free model each request

SCHEMA = """
job_postings_fact(job_id, company_id, job_title_short, job_title, job_location, job_via,
    job_schedule_type, job_work_from_home, search_location, job_posted_date,
    job_no_degree_mention, job_health_insurance, job_country,
    salary_rate, salary_year_avg, salary_hour_avg)
company_dim(company_id, name, link, link_google, thumbnail)
skills_job_dim(index, job_id, skill_id)
skills_dim(index, skill_id, skills, type)
"""

def generate_sql(question: str) -> str:
    prompt = f"""You are a PostgreSQL expert. Schema:
{SCHEMA}
Write ONE SELECT query answering: "{question}"
Output ONLY raw SQL, no markdown fences, no explanation."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    sql = response.choices[0].message.content.strip()
    return sql.replace("```sql", "").replace("```", "").strip()

def summarize_results(question: str, df) -> str:
    if df.empty:
        return "The query returned no results — try rephrasing."
    preview = df.head(20).to_string(index=False)
    prompt = f"""Question: "{question}"
Results:
{preview}
Write a 2-3 sentence plain-English insight. No preamble."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def ask(question: str):
    sql = generate_sql(question)
    df = run_readonly_query(sql)
    summary = summarize_results(question, df)
    return sql, df, summary