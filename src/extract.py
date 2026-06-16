import pandas as pd
import logging

#Config Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)

def load_csv(path, name):
    logger.info(f"Loading {name} from:  {path}")
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logger.error(f"{name} not found at path: {path}")
        raise
    logger.info(f"{name} loaded successfully - {len(df)} records found")
    return df

def validate_dataframe(df, name):
    if df.empty:
        logger.warning(f"{name} is empty")
        return False
    logger.info(f"{name} contains {len(df)} records")
    logger.info(f"Data shape for {name}: {df.shape}")
    logger.info(f"Data null values for {name}:\n{df.isnull().sum()}")
    logger.info(f"Unique job_link in {name}: {df['job_link'].nunique()}")
    return True

def extract_all(raw_path):
    jobs_path = f"{raw_path}/job_postings.csv"
    skills_path = f"{raw_path}/job_skills.csv"
    summary_path = f"{raw_path}/job_summary.csv"

    jobs_df = load_csv(jobs_path, "Job Postings")
    skills_df = load_csv(skills_path, "Job Skills")
    summary_df = load_csv(summary_path, "Job Summary")

    # Validate the loaded dataframes
    validate_dataframe(jobs_df, "Job Postings")
    validate_dataframe(skills_df, "Job Skills")
    validate_dataframe(summary_df, "Job Summary")
    return jobs_df, skills_df, summary_df

if __name__ == "__main__":
    raw_path = "data/raw"
    extract_all(raw_path)
    logger.info("Data extraction completed successfully")
