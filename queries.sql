USE job_market;

-- Query 1: Top 20 most in demand skills
SELECT job_skills, COUNT(*) AS amount
FROM expanded_skills
GROUP BY job_skills
ORDER BY amount DESC
LIMIT 20;

-- Query 2: Top 15 most common job titles
SELECT job_title, COUNT(*) AS amount
FROM cleaned_jobs
GROUP BY job_title
ORDER BY amount DESC
LIMIT 20;

-- Query 3: Top 10 skills by seniority level
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
Where rn <= 10;

-- Query 4: Top 10 skills in US vs. other countries (UK, Canada, Australia)
-- Note: sample outside the US is limited (~16% of total records)
SELECT * FROM (
	SELECT expanded_skills.job_skills,
        CASE
        WHEN cleaned_jobs.search_country = 'united states' THEN 'united states'
        ELSE 'other'
    END AS country_group,
    COUNT(*) as amount,
    ROW_NUMBER() OVER(
		PARTITION BY
			CASE
			WHEN cleaned_jobs.search_country = 'united states' THEN 'united states'
			ELSE 'other'
		END
	ORDER BY COUNT(*) DESC) 
    AS rn
    FROM cleaned_jobs
    LEFT JOIN expanded_skills ON cleaned_jobs.job_link = expanded_skills.job_link
    GROUP BY 
		CASE
			WHEN cleaned_jobs.search_country = 'united states' THEN 'united states'
			ELSE 'other'
		END,
		expanded_skills.job_skills
)ranked
WHERE rn <= 10;