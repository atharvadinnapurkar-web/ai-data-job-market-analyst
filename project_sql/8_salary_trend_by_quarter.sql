/*
Question: How has the average Data Analyst salary trended by quarter?
*/

SELECT
    EXTRACT(YEAR FROM job_posted_date) AS posting_year,
    EXTRACT(QUARTER FROM job_posted_date) AS posting_quarter,
    ROUND(AVG(salary_year_avg), 0) AS avg_salary,
    COUNT(*) AS job_count
FROM
    job_postings_fact
WHERE
    job_title_short = 'Data Analyst'
    AND salary_year_avg IS NOT NULL
GROUP BY
    posting_year,
    posting_quarter
ORDER BY
    posting_year,
    posting_quarter;
