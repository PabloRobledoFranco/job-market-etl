USE job_market;
SHOW TABLES;
DESCRIBE cleaned_jobs;
DESCRIBE expanded_skills;
SELECT COUNT(job_skills) FROM expanded_skills;
SELECT job_skills, COUNT(*) AS amount
FROM expanded_skills
GROUP BY job_skills
ORDER BY amount DESC
LIMIT 20;

SELECT job_title, COUNT(*) AS amount
FROM cleaned_jobs
GROUP BY job_title
ORDER BY amount DESC
LIMIT 20;

SELECT * FROM (
	SELECT 
    expanded_skills.job_skills, 
    cleaned_jobs.job_level, 
    COUNT(*) as amount,
    ROW_NUMBER() OVER(PARTITION BY job_level ORDER BY COUNT(*) DESC) AS rn
	FROM cleaned_jobs
	LEFT JOIN expanded_skills ON cleaned_jobs.job_link = expanded_skills.job_link
	GROUP BY cleaned_jobs.job_level, expanded_skills.job_skills
)ranked 
Where rn <= 10 
