from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from src.data_pipeline import process_sales_data
from src.database import read_sales_data, save_sales_data

st.set_page_config(page_title="Cloud Sales Analytics",page_icon="📊",layout="wide")
st.title("📊 Cloud Sales Analytics")
st.caption("CSV → Python/Pandas → SQLite → Streamlit | Local-only, no AWS resources")
with st.sidebar:
    st.header("Data source")
    choice=st.radio("Choose source",["Included sample dataset","Upload your CSV"])
    uploaded=st.file_uploader("Sales CSV",type=["csv"]) if choice=="Upload your CSV" else None
    st.caption("Processing and storage run on this computer.")
raw=None
if choice=="Included sample dataset":
    raw=pd.read_csv("data/sales_sample.csv")
elif uploaded is not None:
    try: raw=pd.read_csv(uploaded)
    except Exception as e: st.error(f"Unable to read CSV: {e}")
if raw is not None:
    st.subheader("1. Source preview")
    st.write(f"Rows received: **{len(raw):,}**")
    st.dataframe(raw.head(10),use_container_width=True)
    if st.button("Process data and save to SQLite",type="primary"):
        try:
            clean,rejected,dups=process_sales_data(raw)
            save_sales_data(clean)
            st.session_state["quality"]={"input":len(raw),"accepted":len(clean),
                                         "rejected":len(rejected),"duplicates":dups}
            st.session_state["rejected"]=rejected
            st.success(f"Saved {len(clean)} clean records to data/sales_analytics.db")
        except Exception as e: st.error(str(e))
if "quality" in st.session_state:
    q=st.session_state["quality"]; st.subheader("2. Data quality")
    a,b,c,d=st.columns(4)
    a.metric("Input rows",q["input"]); b.metric("Accepted",q["accepted"])
    c.metric("Rejected",q["rejected"]); d.metric("Duplicate IDs",q["duplicates"])
    bad=st.session_state["rejected"]
    if not bad.empty:
        st.warning("Review rejected rows before treating the dataset as clean.")
        st.dataframe(bad,use_container_width=True)
        st.download_button("Download quality report",bad.to_csv(index=False).encode(),
                           "sales_quality_report.csv","text/csv")
sales=read_sales_data()
st.divider(); st.subheader("3. Analytics dashboard")
if sales.empty:
    st.info("Load the sample data or upload a CSV, then click Process data.")
    st.stop()
sales["order_date"]=pd.to_datetime(sales["order_date"])
with st.sidebar:
    st.header("Filters")
    regions=sorted(sales.region.unique())
    chosen_regions=st.multiselect("Region",regions,default=regions)
    # products=sorted(sales.product.unique())
    products = sorted(sales["product"].unique())
    chosen_products=st.multiselect("Product",products,default=products)
# view=sales[sales.region.isin(chosen_regions)&sales.product.isin(chosen_products)].copy()
view = sales[
    sales["region"].isin(chosen_regions) &
    sales["product"].isin(chosen_products)
].copy()
if view.empty: st.warning("No data matches these filters."); st.stop()
revenue=view.revenue.sum(); profit=view.profit.sum(); cost=view.total_cost.sum()
margin=profit/revenue*100 if revenue else 0
k1,k2,k3,k4=st.columns(4)
k1.metric("Revenue",f"₹{revenue:,.0f}"); k2.metric("Profit",f"₹{profit:,.0f}")
k3.metric("Cost",f"₹{cost:,.0f}"); k4.metric("Profit margin",f"{margin:.1f}%")
view["month"]=view.order_date.dt.to_period("M").astype(str)
monthly=view.groupby("month",as_index=False).agg(Revenue=("revenue","sum"),Profit=("profit","sum"))
x,y=st.columns(2)
x.plotly_chart(px.line(monthly,x="month",y="Revenue",markers=True,title="Monthly revenue"),use_container_width=True)
reg=view.groupby("region",as_index=False).revenue.sum().sort_values("revenue",ascending=False)
y.plotly_chart(px.bar(reg,x="region",y="revenue",title="Revenue by region"),use_container_width=True)
x,y=st.columns(2)
prod=view.groupby("product",as_index=False).profit.sum().sort_values("profit",ascending=False)
x.plotly_chart(px.bar(prod,x="product",y="profit",title="Profit by product"),use_container_width=True)
channel=view.groupby("sales_channel",as_index=False).revenue.sum()
y.plotly_chart(px.pie(channel,names="sales_channel",values="revenue",title="Revenue by channel"),use_container_width=True)
st.subheader("4. Transaction details")
display=view.drop(columns=["month"],errors="ignore")
st.dataframe(display,use_container_width=True)
st.download_button("Download filtered clean data",display.to_csv(index=False).encode(),
                   "clean_sales_data.csv","text/csv")
