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
    return create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

def run_query(query, engine, name):
    
    