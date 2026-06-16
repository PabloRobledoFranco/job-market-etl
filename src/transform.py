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