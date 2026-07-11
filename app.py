import streamlit as st
st.set_page_config(page_title="Sales Dashboard",
                   layout="wide")
st.title("Sales Performance Dashboard")
st.caption("Interactive Sales Dashboard | Built using Python,Streamlit & Plotly")


import pandas as pd
df=pd.read_csv("sales_data_sample.csv",encoding="latin1")
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])

df["YEAR"] = df["ORDERDATE"].dt.year
df["MONTH"] = df["ORDERDATE"].dt.month
df["MONTH_NAME"] = df["ORDERDATE"].dt.month_name()
df["QUARTER"] = df["ORDERDATE"].dt.quarter

st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",["All"]+
    sorted(df["YEAR"].unique())
)


selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["COUNTRY"].unique().tolist())
)


selected_product = st.sidebar.selectbox(
    "Select Product Line",
    ["All"] + sorted(df["PRODUCTLINE"].unique().tolist())
)

if selected_year=="All":
   filtered_df=df.copy()
else:
   filtered_df = df[df["YEAR"]==selected_year]
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["COUNTRY"] == selected_country]

if selected_product != "All":
    filtered_df = filtered_df[filtered_df["PRODUCTLINE"] == selected_product]
total_sales = filtered_df["SALES"].sum()
total_orders = filtered_df["ORDERNUMBER"].nunique()
total_customers = filtered_df["CUSTOMERNAME"].nunique()
total_quantity = filtered_df["QUANTITYORDERED"].sum()

st.subheader("Key Performance Indicators")
col1,col2,col3,col4=st.columns(4)

with col1: st.metric("Total Sales",f"${total_sales:,.0f}")

with col2: st.metric("Total Orders",total_orders)

with col3: st.metric("Total Customers",total_customers)
with col4: st.metric("Quantities Sold",total_quantity)

sales_by_product = (filtered_df.groupby("PRODUCTLINE")["SALES"].sum().reset_index())
import plotly.express as px
fig=px.bar(sales_by_product,x="PRODUCTLINE",y="SALES",title="Sales by Product Line")
fig.update_traces(texttemplate="$%{y:,.0f}",textposition="outside")
fig.update_layout(xaxis_title="Product Line",yaxis_title="Total Sles",yaxis_tickformat=",.0f")


month_order=["January","February","March","April","May","June","July","August","September","October","November","December"]
monthly_sales=(filtered_df.groupby("MONTH_NAME")["SALES"].sum().reset_index())
monthly_sales["MONTH_NAME"]=pd.Categorical(monthly_sales["MONTH_NAME"],categories=month_order,ordered=True)
monthly_sales=monthly_sales.sort_values("MONTH_NAME")

fig_month=px.line(monthly_sales,x="MONTH_NAME",y="SALES",markers=True,title="Monthly Sales Trend")
fig_month.update_layout(xaxis_title="Month",yaxis_title="Total Sales",yaxis_tickformat=",.0f")


col1,col2=st.columns(2)

with col1:st.plotly_chart(fig,use_container_width=True)
with col2:st.plotly_chart(fig_month,use_container_width=True)

sales_by_country=(filtered_df.groupby("COUNTRY")["SALES"].sum().reset_index())
fig_country=px.bar(sales_by_country,x="COUNTRY",y="SALES",color="COUNTRY",color_discrete_sequence=px.colors.qualitative.Set3,
                                    text="SALES",title="Sales by Country")
fig_country.update_traces(texttemplate="$%{y:,.0f}",textposition="outside")
fig_country.update_layout(yaxis_tickformat=",.0f")

top_customers=filtered_df.groupby("CUSTOMERNAME")["SALES"].sum().sort_values(ascending=False).head(10).reset_index()
fig_customers=px.bar(top_customers,y="CUSTOMERNAME",x="SALES",orientation="h",color="CUSTOMERNAME",
                                  color_discrete_sequence=px.colors.qualitative.Set3,title="Top 10 Customers")
fig_customers.update_layout(xaxis_tickformat=",.0f")

col3,col4=st.columns(2)

with col3: st.plotly_chart(fig_country,use_container_width=True)
with col4: st.plotly_chart(fig_customers,use_container_width=True)

status_sales=(filtered_df.groupby("STATUS")["SALES"].sum().reset_index())
fig_status=px.pie(status_sales,names="STATUS",values="SALES",hole=0.5,color="STATUS",
                               color_discrete_sequence=px.colors.qualitative.Set2,title="Sales by Order Status")
fig_status.update_traces(textinfo="percent+label")

deal_size=(filtered_df.groupby("DEALSIZE")["SALES"].sum().reset_index())

fig_deal=px.bar(deal_size,x="DEALSIZE",y="SALES",color="DEALSIZE",
                          color_discrete_sequence=px.colors.qualitative.Set2,text="SALES",title="Sales by Del Size")
fig_deal.update_traces(texttemplate="$%{y:,.0f}",textposition="outside")

col5,col6=st.columns(2)

with col5: st.plotly_chart(fig_status,use_container_width=True)
with col6: st.plotly_chart(fig_deal,use_container_width=True)

csv=filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(label="Download Filtered Data",data=csv, file_name="filtered_sales.csv",mime="text/csv")