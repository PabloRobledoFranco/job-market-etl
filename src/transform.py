import logging
import pandas as pd

#Config Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)

def merge_dataframes(jobs_df, skills_df, summary_df):
    logger.info("Merging dataframes")
    merged = pd.merge(jobs_df, skills_df, on="job_link", how="inner")
    merged = pd.merge(merged, summary_df, on="job_link", how="inner")
    logger.info(f"Merged dataframe shape: {merged.shape}")
    return merged

def clean_text_columns(df):
    logger.info("Cleaning text columns")
    df = df.copy()  # Avoid modifying original dataframe
    text_columns = ['job_title', 'job_level', 'job_type', 'search_country', 'search_city']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower()
    logger.info("Text columns cleaned")
    return df

def expand_skills(df):
    nulls = df["job_skills"].isnull().sum()
    if nulls > 0:
        logger.warning(f"Dropping {nulls} null values in 'job_skills' column")
        df = df.dropna(subset=["job_skills"])

    logger.info("Expanding skills into separate rows")
    df = df.copy()  # Avoid modifying original dataframe
    df["job_skills"] = df["job_skills"].str.split(",")
    df = df.explode("job_skills").reset_index(drop=True)
    df["job_skills"] = df["job_skills"].str.strip().str.lower()
    logger.info(f"Dataframe shape after expanding skills: {df.shape}")
    return df

def transform_all(jobs_df, skills_df, summary_df):
    merged_df = merge_dataframes(jobs_df, skills_df, summary_df)
    cleaned_df = clean_text_columns(merged_df)
    expanded_skills_df = expand_skills(cleaned_df)
    return cleaned_df, expanded_skills_df

if __name__ == "__main__":
    from extract import extract_all

    jobs_df, skills_df, summary_df = extract_all("data/raw")
    cleaned_df, expanded_skills_df = transform_all(jobs_df, skills_df, summary_df)
    
    logger.info(f"Merged DataFrame shape: {cleaned_df.shape}")
    logger.info(f"Skills expanded DataFrame shape: {expanded_skills_df.shape}")