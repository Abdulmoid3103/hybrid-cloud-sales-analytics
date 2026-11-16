import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH=Path("data/sales_analytics.db")

def connect(path=DB_PATH):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    return sqlite3.connect(p)

def save_sales_data(df,path=DB_PATH):
    with connect(path) as con:
        df.to_sql("sales",con,if_exists="replace",index=False)
        con.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region)")
    return len(df)

def read_sales_data(path=DB_PATH):
    if not Path(path).exists(): return pd.DataFrame()
    with connect(path) as con:
        try: return pd.read_sql_query("SELECT * FROM sales ORDER BY order_date",con)
        except sqlite3.OperationalError: return pd.DataFrame()
