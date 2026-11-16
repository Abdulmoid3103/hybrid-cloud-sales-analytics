import pandas as pd

REQUIRED = ["order_id","order_date","customer_id","product","category","region","city",
            "sales_channel","quantity","unit_price","unit_cost"]
NUMERIC = ["quantity","unit_price","unit_cost"]

def process_sales_data(data):
    """Return (cleaned, rejected, duplicate_count); never silently discard bad rows."""
    if data is None or data.empty:
        raise ValueError("The CSV has no data rows.")
    missing=[c for c in REQUIRED if c not in data.columns]
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))
    df=data[REQUIRED].copy()
    df["_source_row"]=range(2,len(df)+2)
    for c in REQUIRED:
        if c not in NUMERIC:
            df[c]=df[c].astype("string").str.strip()
    df["order_date"]=pd.to_datetime(df["order_date"],errors="coerce")
    for c in NUMERIC:
        df[c]=pd.to_numeric(df[c],errors="coerce")
    valid=pd.Series(True,index=df.index)
    for c in ["order_id","customer_id","product","category","region","city","sales_channel"]:
        valid &= df[c].notna() & df[c].ne("")
    valid &= df["order_date"].notna()
    for c in NUMERIC: valid &= df[c].notna()
    valid &= df["quantity"].gt(0) & df["unit_price"].gt(0)
    valid &= df["unit_cost"].ge(0) & df["unit_cost"].le(df["unit_price"])
    rejected=df.loc[~valid].copy()
    if not rejected.empty: rejected["rejection_reason"]="Missing or invalid required value"
    good=df.loc[valid].copy()
    dup=good.duplicated("order_id",keep="first")
    duplicates=good.loc[dup].copy()
    if not duplicates.empty: duplicates["rejection_reason"]="Duplicate order_id; first valid row retained"
    clean=good.loc[~dup].copy()
    clean["order_date"]=clean["order_date"].dt.strftime("%Y-%m-%d")
    clean["quantity"]=clean["quantity"].astype(int)
    clean["revenue"]=clean["quantity"]*clean["unit_price"]
    clean["total_cost"]=clean["quantity"]*clean["unit_cost"]
    clean["profit"]=clean["revenue"]-clean["total_cost"]
    clean["profit_margin_pct"]=(clean["profit"]/clean["revenue"]*100).round(2)
    rejected=pd.concat([rejected,duplicates],ignore_index=True)
    cols=REQUIRED+["revenue","total_cost","profit","profit_margin_pct"]
    return clean[cols].reset_index(drop=True), rejected.reset_index(drop=True), int(dup.sum())
