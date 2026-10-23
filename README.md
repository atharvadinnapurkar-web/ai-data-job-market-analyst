# 📊 AI Data Job Market Analyst

Ask a plain-English question about the data job market. An LLM writes the SQL, the app runs it live against a PostgreSQL database, and the results come back with a plain-English explanation.

**🎥 Demo:** see the walkthrough video in my LinkedIn post _(add link)_

![demo gif placeholder](assets/demo.gif)

---

## Why this project

Most "data analyst SQL project" repos follow the same shape: write some queries, screenshot the output, done. This one goes a step further and wraps the analysis in an AI layer, so it works as a tool rather than a one-off report:

- Type a question in plain English and an LLM converts it into a SQL query
- The query runs live against a real job postings database
- The results come back with an AI-written insight, and the generated SQL is always shown so you can verify exactly what ran

The AI layer sits on top of genuine relational SQL work (fact table + dimension tables), not instead of it.

## Architecture

```
User question (plain English)
        │
        ▼
  LLM via OpenRouter (text-to-SQL)  ──▶  generates a single SELECT query
        │
        ▼
  Safety guardrail (db.py)  ──▶  allows read-only SELECT statements only
        │
        ▼
  PostgreSQL database  ──▶  executes the query
        │
        ▼
  LLM via OpenRouter (summarization)  ──▶  writes a plain-English insight
        │
        ▼
  Streamlit UI  ──▶  shows the SQL, results table, chart, and insight
```

## Tech stack

- **PostgreSQL**: the job postings dataset
- **Python**: `pandas`, `sqlalchemy`, `psycopg`
- **OpenRouter**: one OpenAI-compatible API giving access to many LLMs, including free ones (used via the `openai` Python SDK)
- **Streamlit**: interactive front end
- **Plotly**: charts

## Database schema

| Table | Purpose |
|---|---|
| `job_postings_fact` | One row per job posting: title, location, salary, dates, etc. |
| `company_dim` | Company details |
| `skills_job_dim` | Bridge table linking job postings to skills (many-to-many) |
| `skills_dim` | Skill names and skill types |

## Features

### 🤖 Ask the AI Analyst
Type a question like "Which skills pay the most for remote Data Analyst roles?" and get the generated SQL, a results table, an auto-generated chart, and a written insight.

### 📌 Hand-written SQL analysis (`project_sql/`)
Eight queries covering the classic analyst questions plus three deeper ones:

1. Top-paying Data Analyst jobs
2. Skills required for the top-paying jobs (CTE)
3. Most in-demand skills
4. Skills with the highest average salary
5. Most "optimal" skills: high demand and high salary (`HAVING`)
6. **Top 3 skills per job title**: window function (`DENSE_RANK() OVER (PARTITION BY ...)`)
7. **Skill co-occurrence**: which skill pairs appear together most often (self-join)
8. **Quarterly salary trend**: average salary over time (date functions)

### 🔒 Guardrails
Because an LLM generates the SQL from free text, `src/db.py` enforces:
- Only `SELECT` statements are allowed
- Forbidden keywords (`INSERT`, `UPDATE`, `DELETE`, `DROP`, etc.) are blocked
- Multiple/stacked statements are rejected

## Setup

```bash
git clone <your-repo-url>
cd ai-data-job-market-analyst

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root (never commit it):

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

- Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys)
- If your database password contains special characters (like `@`), URL-encode it, e.g. `@` becomes `%40`

Then run:

```bash
streamlit run app.py
```

### Changing the model
The model is set by one constant (`MODEL`) in `src/ai_analyst.py`. It defaults to `openrouter/free`, which routes each request to an available free model. Swap in any other OpenRouter model ID if you want more consistent results.

## Limitations

- **Free models can write imperfect SQL.** Quality varies because `openrouter/free` rotates between models. That's why the app always shows the generated query; if a result looks off, ask again or rephrase.
- The app runs against a **local** PostgreSQL database, so it isn't publicly hosted. See the demo video above.

## Key insights from the analysis

_Fill this in after running the queries on your data. Example bullets:_

- Top-paying remote Data Analyst roles range from $X to $Y
- SQL and Python dominate both the top-paying and most in-demand skill lists
- [Skill A] and [Skill B] co-occur in more postings than any other pair
- Average salaries [rose / fell / stayed flat] across the quarters in the dataset

## What I learned

- Writing advanced SQL: CTEs, subqueries, window functions, self-joins, `UNION`
- Designing guardrails for LLM-generated SQL running against a real database
- Wiring an LLM into a data pipeline via an OpenAI-compatible API
- Building an interactive Streamlit app
- Handling secrets safely (`.env`, `.gitignore`, and rotating keys after an accidental leak)

## Future improvements

- Host the database in the cloud (e.g. Neon) and deploy the app publicly
- Cache repeated questions to cut down on API calls
- Add a salary prediction model (regression on skills + location)
- Support follow-up questions (multi-turn conversation)
- Add rate limiting before making a demo public

---

*Dataset from [Luke Barousse's SQL course](https://www.lukebarousse.com/). The AI layer, deeper SQL analysis, and app were built on top of it as an independent project.*
