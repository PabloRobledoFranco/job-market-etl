# - Data Science Job Market ETL Pipeline-

End-to-end ETL pipeline that pulls 12,217 data science job postings from LinkedIn (via Kaggle), cleans and transforms them, loads everything into MySQL, and runs SQL analysis to figure out what skills the market actually wants.

## Tech Stack

- **Python** — pandas, SQLAlchemy, python-dotenv
- **MySQL 8.0** — data storage and SQL analysis
- **Jupyter Notebook** — exploratory data analysis

## Pipeline Architecture

```
data/raw/
    (3 CSV files)
        - job_posting.csv
        - job_skills.csv
        - job_summary.csv
↓
extract.py →→ Load and validates de raw CSV data.
↓
transform.py →→ Merge → Clean → Explode the skills into rows.
↓
load.py →→ Export processed CSVs → load to MySQL
↓
MySQL Database
    - cleaned_jobs (~ 12.000 rows)
    - expanded_skills (~ 314.000 rows)
↓
queries.sql →→ 4 analytical SQL queries
↓
analyze.py →→ Execute queries and display results
```

## Project Structure

```
job-market-etl/
├── data/
│   ├── raw/              ← Original Kaggle CSVs (not tracked by git)
│   └── processed/        ← Cleaned CSVs output (not tracked by git)
├── notebooks/
│   └── explore.ipynb     ← Exploratory data analysis
├── src/
│   ├── extract.py        ← Load and validate raw data
│   ├── transform.py      ← Merge, clean, and explode skills
│   ├── load.py           ← Export to CSV and load into MySQL
│   └── analyze.py        ← Execute SQL queries and display results
├── queries.sql           ← 4 analytical SQL queries
├── .env                  ← MySQL credentials (not tracked by git)
├── requirements.txt
└── README.md
```

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/PabloRobledoFranco/job-market-etl.git
cd job-market-etl
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up credentials
Create a `.env` file in the project root:
→ MYSQL_USER = (your mysql user) → MYSQL_PASSWORD = (your mysql password)

### 4. Download the dataset
Download from Kaggle (https://www.kaggle.com/datasets/asaniczka/data-science-job-postings-and-skills) and drop the 3 CSV files into `data/raw/`.

### 5. Run the pipeline
```bash
python src/load.py      # Extract, transform, and load to MySQL
python src/analyze.py   # Run SQL analysis and display results
```

## Analysis Questions

1. What are the most in-demand skills in data science?
2. What job titles have the most postings?
3. Do required skills differ by seniority level?
4. Is there a difference in skill demand between the US and other markets?

## Key Findings

Based on 12,217 job postings — 84% US, the rest spread across UK, Canada, and Australia

**1. Most in-demand skills**
Python and SQL are far ahead of everything else — 4,810 and 4,610 mentions respectively, nearly double Data Analysis (3,293) in third place. No surprises there, but the gap is bigger than expected.

**2. Most common job titles**
The dataset skews senior. Senior Data Engineer leads with 288 postings, followed by Senior Data Analyst (165) and Data Engineer (150). Entry-level roles are underrepresented — which might say something about where LinkedIn job postings tend to cluster.

**3. Skills by seniority**
Associate and Mid-Senior levels both prioritize SQL, Python, and Data Analysis. The difference kicks in at Mid-Senior: AWS, Data Engineering, and Project Management start showing up — meaning cloud and infrastructure knowledge becomes expected, not optional.

**4. US vs. other markets**
The core stack (Python, SQL, Data Analysis) is consistent everywhere. What changes: the US specifically pushes AWS and Data Engineering into the top 10, while UK/Canada/Australia lean more toward Power BI and Tableau. BI tools seem to matter more outside the US.

> Non-US sample is small (~16% of records) and limited to English-speaking Western markets — take regional comparisons with that in mind.

## Design Decisions

- **MySQL over SQLite** — SQLite is fine for prototypes, but MySQL is what you'd actually run in production. Using it locally felt like the right call for a project about job market skills.
- **Modular pipeline** — Each ETL phase has its own file (extract, transform, load, analyze). It's a bit more setup upfront, but way easier to debug and extend than a single monolithic script.
- **Skills explode** — Raw data stores skills as comma-separated strings per job. Exploding them into individual rows is what makes SQL frequency analysis actually work cleanly.
- **dotenv for credentials** — MySQL credentials live in a `.env` file that never gets committed. Basic security practice, but worth being explicit about it.

## Data Source

Dataset: [Data Science Job Postings & Skills (2024)](https://www.kaggle.com/datasets/asaniczka/data-science-job-postings-and-skills/data) by asaniczka on Kaggle. Data collected from LinkedIn job postings.
