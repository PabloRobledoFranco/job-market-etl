import logging
import pandas as pd
import os
from sqlalchemy import create_engine 
from dotenv import load_dotenv

#Config Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


#Engine for MySQL connection

def get_engine():
    load_dotenv()  # Load environment variables from .env file
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = "localhost"
    database ="job_market"
    try:
        engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
        logger.info("Successfully connected to the database.")
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        raise
    return engine

def run_query(query, engine, name):
    logger.info(f"Running query for {name}...")
    df = pd.read_sql(query, engine)
    logger.info(f"Query for {name} completed. Retrieved {len(df)} records.")
    logger.info(f"DataFrame:\n{df.head()}")
    return df

def top_skills(engine):
    query ="""
    SELECT job_skills, COUNT(*) AS amount
    FROM expanded_skills
    GROUP BY job_skills
    ORDER BY amount DESC
    LIMIT 20;
    """
    return run_query(query, engine, "Q1 - Top Skills")

def top_job_titles(engine):
    query ="""
    SELECT job_title, COUNT(*) AS amount
    FROM cleaned_jobs
    GROUP BY job_title
    ORDER BY amount DESC
    LIMIT 20;
    """
    return run_query(query, engine, "Top Job Titles")

def skills_by_seniority(engine):
    query ="""
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
    """
    return run_query(query, engine, "Q3 - Skills by Seniority")

def skills_by_country_group(engine):
    query ="""
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
    """
    return run_query(query, engine, "Q4 - Skills by Country Group")

def analyze_all():
    engine = get_engine()
    top_skills_df = top_skills(engine)
    top_job_titles_df = top_job_titles(engine)
    skills_by_seniority_df = skills_by_seniority(engine)
    skills_by_country_group_df = skills_by_country_group(engine)

    return {
        "top_skills": top_skills_df,
        "top_job_titles": top_job_titles_df,
        "skills_by_seniority": skills_by_seniority_df,
        "skills_by_country_group": skills_by_country_group_df
    }

if __name__ == "__main__":
    results = analyze_all()

    logger.info("\n--- Q1 - TOP 20 SKILLS ---\n")
    print(results["top_skills"].to_string(index=False))

    logger.info("\n--- Q2 - TOP 20 JOB TITLES ---\n")
    print(results["top_job_titles"].to_string(index=False))

    logger.info("\n--- Q3 - TOP 10 SKILLS BY SENIORITY ---\n")
    print(results["skills_by_seniority"].to_string(index=False))

    logger.info("\n--- Q4 - TOP 10 SKILLS BY COUNTRY GROUP ---\n")
    print(results["skills_by_country_group"].to_string(index=False))