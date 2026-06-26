import logging
import pandas as pd
import os
import mysql.connector
from sqlalchemy import create_engine 
from dotenv import load_dotenv

#Config Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)

def save_csv(df, path, name):
    logger.info(f"Saving {name} to: {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        logger.error(f"Failed to save {name} to {path}: {e}")
        raise
    logger.info(f"{name} saved successfully to: {path}")
    logger.info(f"{name} shape: {df.shape}")

def load_all(cleaned_df, expanded_skills_df, processed_path):
    logger.info("Starting to load dataframes to CSV files")
    
    save_csv(cleaned_df, f"{processed_path}/cleaned_jobs.csv", "Cleaned Jobs DataFrame")
    save_csv(expanded_skills_df[["job_link", "job_skills"]], f"{processed_path}/expanded_skills.csv", "Expanded Skills DataFrame")
    logger.info("All dataframes loaded successfully to CSV files")

def get_mysql_conection(host, user, password, database):
    logger.info(f"Connecting to MySQL database: {database} at {host} with user {user}")
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        logger.info("MySQL connection established successfully")
        return connection
    except mysql.connector.Error as e:
        logger.error(f"Error connecting to MySQL, Error: {e}")
        raise

def load_to_mysql(cleaned_df, expanded_skills_df, user, password, host="localhost", database="job_market"):
    logger.info("Loading dataframes to MySQL database")
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    cleaned_df.to_sql("cleaned_jobs", con=engine, if_exists="replace", index=False)
    logger.info(f"cleaned_jobs loaded - {len(cleaned_df)} rows")
    expanded_skills_df[["job_link", "job_skills"]].to_sql("expanded_skills", con=engine, if_exists="replace", index=False)
    logger.info(f"expanded_skills loaded - {len(expanded_skills_df)} rows")

if __name__ == "__main__":
    from transform import transform_all
    from extract import extract_all

    load_dotenv()  # Load environment variables from .env file

    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")

    raw_path = "data/raw"
    processed_path = "data/processed"

    jobs_df, skills_df, summary_df = extract_all(raw_path)
    
    cleaned_df, expanded_skills_df = transform_all(jobs_df, skills_df, summary_df)
    


    load_all(cleaned_df, expanded_skills_df, processed_path)

    load_to_mysql(cleaned_df, expanded_skills_df, user=user, password=password)

    logger.info("MySQL loading process completed successfully")

    logger.info("Data loading process completed successfully")