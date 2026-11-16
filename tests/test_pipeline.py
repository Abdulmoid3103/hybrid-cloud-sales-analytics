import unittest
import pandas as pd
from src.data_pipeline import process_sales_data

def row(order_id="A1"):
    return {"order_id":order_id,"order_date":"2025-01-01","customer_id":"C1",
            "product":"Keyboard","category":"Accessories","region":"West","city":"Pune",
            "sales_channel":"Online","quantity":2,"unit_price":1000,"unit_cost":600}

class TestPipeline(unittest.TestCase):
    def test_financial_metrics(self):
        clean,bad,dups=process_sales_data(pd.DataFrame([row()]))
        self.assertEqual(len(clean),1); self.assertEqual(clean.iloc[0].revenue,2000)
        self.assertEqual(clean.iloc[0].profit,800); self.assertEqual(clean.iloc[0].profit_margin_pct,40)
    def test_duplicate_detection(self):
        clean,bad,dups=process_sales_data(pd.DataFrame([row(),row()]))
        self.assertEqual(len(clean),1); self.assertEqual(dups,1); self.assertEqual(len(bad),1)
    def test_invalid_quantity_rejected(self):
        r=row(); r["quantity"]="bad"
        clean,bad,dups=process_sales_data(pd.DataFrame([r]))
        self.assertEqual(len(clean),0); self.assertEqual(len(bad),1)
    def test_missing_column_error(self):
        with self.assertRaisesRegex(ValueError,"Missing required column"):
            process_sales_data(pd.DataFrame([{"order_id":"x"}]))
if __name__=="__main__": unittest.main()
