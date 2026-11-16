# Architecture: working local pipeline + AWS reference design

## 1. Working local implementation

```text
Sales CSV → Python + Pandas validation/cleaning → SQLite database → Streamlit dashboard
```

The local pipeline validates the required schema, dates and numeric values; rejects invalid rows; detects duplicate order IDs; calculates revenue, cost, profit and margin; saves clean rows to SQLite; and displays interactive dashboard charts.

## 2. AWS architecture (documentation only)

```text
Sales CSV export
      |
      v
Amazon S3 (raw/ prefix)
      |
      | S3 ObjectCreated event
      v
AWS Lambda (validate + transform)
      |
      v
Amazon S3 (curated/ prefix, preferably Parquet)
      |
      v
AWS Glue Data Catalog
      |
      v
Amazon Athena (SQL analytics)
      |
      v
Exported query results / compatible BI tool
```

**This is a conceptual design only. Nothing is deployed.** This project creates no S3 bucket, Lambda function, Glue catalog/crawler, Athena workgroup, IAM role, or other AWS resource.

## 3. Local-to-cloud mapping

| Local project component | AWS concept |
|---|---|
| `data/sales_sample.csv` | S3 raw prefix |
| `src/data_pipeline.py` | Lambda transformation logic |
| SQLite `sales` table | Curated S3 dataset + Glue/Athena table |
| `sql/schema_and_analysis.sql` | Athena SQL concepts |
| Streamlit dashboard | BI/reporting layer |

S3 stores source and curated files; an object-created event can trigger Lambda; Glue provides table metadata; Athena queries files in S3. A real deployment also needs least-privilege IAM, encryption, logging, schema evolution, idempotency, retention and access controls.
