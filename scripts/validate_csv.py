import argparse
import pandas as pd
from src.data_pipeline import process_sales_data

parser=argparse.ArgumentParser(description="Validate a sales CSV")
parser.add_argument("csv_path")
args=parser.parse_args()
clean,rejected,duplicates=process_sales_data(pd.read_csv(args.csv_path))
clean.to_csv("clean_sales_data.csv",index=False)
print(f"Input: {len(clean)+len(rejected)} | Accepted: {len(clean)} | Rejected: {len(rejected)} | Duplicates: {duplicates}")
if not rejected.empty: rejected.to_csv("sales_quality_report.csv",index=False)
print("Created clean_sales_data.csv and (when needed) sales_quality_report.csv")
