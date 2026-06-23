import logging
import pandas as pd

#Config Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger=logging.getLogger(__name__)

def save_csv(df, path, name):
    logger.info(f"Saving {name} to: {path}")
    try:
        df.to_csv(path, index=False)
    except Exception as e:
        logger.error(f"Failed to save {name} to {path}: {e}")
        raise
    logger.info(f"{name} saved successfully to: {path}")
    logger.info(f"{name} shape: {df.shape}")

def load_all(cleaned_df, expanded_skills_df, processed_path):
    