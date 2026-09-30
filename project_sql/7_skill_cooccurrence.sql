/*
Question: Which pairs of skills most frequently appear together
in the SAME job posting? (e.g. does "SQL" often show up alongside "Python"?)

Approach: self-join skills_job_dim to itself on job_id, pairing every skill
in a posting with every other skill in that same posting. The condition
sjd1.skill_id < sjd2.skill_id guarantees each pair is only counted once
(avoids both "SQL-Python" and "Python-SQL", and avoids pairing a skill
with itself).
*/

SELECT
    skill_a.skills AS skill_1,
    skill_b.skills AS skill_2,
    COUNT(*) AS times_paired
FROM
    skills_job_dim AS sjd1
INNER JOIN skills_job_dim AS sjd2
    ON sjd1.job_id = sjd2.job_id
    AND sjd1.skill_id < sjd2.skill_id
INNER JOIN skills_dim AS skill_a
    ON sjd1.skill_id = skill_a.skill_id
INNER JOIN skills_dim AS skill_b
    ON sjd2.skill_id = skill_b.skill_id
GROUP BY
    skill_a.skills,
    skill_b.skills
ORDER BY
    times_paired DESC
LIMIT 20;
