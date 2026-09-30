/*
Question: What are the top 3 most in-demand skills for EACH job title
(Data Analyst, Data Engineer, Data Scientist, etc.) in a single query?

This goes beyond a plain GROUP BY: a window function (DENSE_RANK) ranks
skills WITHIN each job_title_short group, so we get a per-category top-N
in one pass instead of running a separate query per title.
*/

WITH skill_demand AS (
    SELECT
        job_postings_fact.job_title_short,
        skills_dim.skills,
        COUNT(*) AS demand_count
    FROM
        job_postings_fact
    INNER JOIN skills_job_dim
        ON job_postings_fact.job_id = skills_job_dim.job_id
    INNER JOIN skills_dim
        ON skills_job_dim.skill_id = skills_dim.skill_id
    GROUP BY
        job_postings_fact.job_title_short,
        skills_dim.skills
),

ranked_skills AS (
    SELECT
        job_title_short,
        skills,
        demand_count,
        DENSE_RANK() OVER (
            PARTITION BY job_title_short
            ORDER BY demand_count DESC
        ) AS skill_rank
    FROM
        skill_demand
)

SELECT
    job_title_short,
    skills,
    demand_count,
    skill_rank
FROM
    ranked_skills
WHERE
    skill_rank <= 3
ORDER BY
    job_title_short,
    skill_rank;
