# Zero-Cost Hybrid Cloud Sales Analytics Project

A complete, beginner-friendly portfolio project with a **working local pipeline** and **AWS architecture/deployment documentation**. It uses Python, Pandas, SQLite and Streamlit locally. No AWS resources are created, no cloud deployment is required, and no paid service is needed.

## Architecture

**Working locally:** `Sales CSV → Python/Pandas ETL → SQLite → Streamlit dashboard`

**AWS reference only:** `S3 raw → S3 event → Lambda → S3 curated → Glue Catalog → Athena → BI/export`

The AWS design is documentation only. Do not deploy it for this zero-cost version. AWS Free Tier is not a guaranteed ₹0 service.

## Features
- Upload your own CSV or use 150 fictional sample sales records.
- Validate required fields, dates and numeric values.
- Detect duplicate order IDs and report invalid rows.
- Calculate revenue, cost, profit and profit margin.
- Store clean records in a local SQLite database.
- Interactive Streamlit dashboard with filters, KPI cards and charts.
- Download cleaned data and quality reports.
- Unit tests and GitHub Actions workflow.

## Folder structure
```text
Hybrid_Cloud_Sales_Analytics_Project/
├── app.py
├── requirements.txt
├── data/                 # sample CSVs; local SQLite DB is generated here
├── src/                  # ETL and SQLite functions
├── tests/                # unit tests
├── scripts/              # command-line CSV validator
├── sql/                  # schema and sample analysis queries
├── docs/                 # AWS architecture, deployment guide, data dictionary
└── .github/workflows/    # automated tests
```

## Windows setup (step by step)

### 1. Install Python
Install Python 3.10 or later. During setup, select **Add Python to PATH**.
Open PowerShell and check:
```powershell
py --version
```

### 2. Open the extracted folder
Extract this ZIP, open `Hybrid_Cloud_Sales_Analytics_Project` in VS Code, then select **Terminal → New Terminal**.

### 3. Create and activate a virtual environment
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If activation is blocked, install using the venv's Python directly:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Install libraries
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Run automated tests
```powershell
python -m unittest discover -s tests -v
```

### 6. Start the dashboard
```powershell
python -m streamlit run app.py
```
Open the local address shown in the terminal (normally `http://localhost:8501`). Press `Ctrl+C` in the terminal to stop.

### 7. Use the dashboard
1. Choose **Included sample dataset** or **Upload your CSV** in the sidebar.
2. Preview the incoming data.
3. Click **Process data and save to SQLite**.
4. Review the data-quality counts and rejected-row report.
5. Explore KPI cards, region/product filters and charts.
6. Download the filtered clean data if required.

The database is generated at `data/sales_analytics.db`. It is local and excluded from Git.

## Optional command-line validation
```powershell
python scripts/validate_csv.py data/sales_sample.csv
```
This writes `clean_sales_data.csv` and, when necessary, `sales_quality_report.csv` in the project root.

## Publish to GitHub
Create a new public repository on GitHub, then run in the project folder:
```powershell
git init
git add .
git commit -m "Build zero-cost sales analytics pipeline"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/zero-cost-cloud-sales-analytics.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. Never commit real customer data, credentials or the generated SQLite database.

## Cost and scope
- Local Python packages, SQLite, Streamlit, VS Code and GitHub public repositories can be used without a paid subscription.
- Internet access is needed to install dependencies and optionally push to GitHub.
- This project does not deploy to AWS. Review `docs/aws_deployment_guide.md` for a future learning plan and cost/security warnings.
