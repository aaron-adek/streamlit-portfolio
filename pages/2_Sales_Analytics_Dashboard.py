import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sidebar import render_sidebar

st.set_page_config(page_title="Sales Analytics | Aaron Adekoya", page_icon="A", layout="wide")
render_sidebar()

# ── Load data ───────────────────────────────────────────────────────────────────
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sales_data.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df["profit"] = df["revenue"] - df["cost"]
    df["margin_pct"] = (df["profit"] / df["revenue"] * 100).round(1)
    df["month"] = df["date"].dt.strftime("%b %Y")
    return df


df = load_data()

# ── Page header ─────────────────────────────────────────────────────────────────
st.title("Sales Analytics Dashboard")
st.markdown(
    """
    Explore revenue, profit, and unit sales across EMEIA regions,
    product categories, and sales channels. Use the filters below to
    drill into specific segments — the KPIs, charts, and margin heatmap
    will update automatically.
    """
)

# ── Filters ─────────────────────────────────────────────────────────────────────
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    regions = st.multiselect(
        "Region",
        options=sorted(df["region"].unique()),
        default=sorted(df["region"].unique()),
    )
with col_f2:
    categories = st.multiselect(
        "Product Category",
        options=sorted(df["product_category"].unique()),
        default=sorted(df["product_category"].unique()),
    )
with col_f3:
    channels = st.multiselect(
        "Channel",
        options=sorted(df["channel"].unique()),
        default=sorted(df["channel"].unique()),
    )

# Apply filters
mask = (
    df["region"].isin(regions)
    & df["product_category"].isin(categories)
    & df["channel"].isin(channels)
)
filtered = df[mask].copy()

if filtered.empty:
    st.warning("No data matches the current filters. Adjust your selections above.")
    st.stop()

# ── KPI Cards ───────────────────────────────────────────────────────────────────
st.markdown("### Key Performance Indicators")

total_revenue = filtered["revenue"].sum()
total_profit = filtered["profit"].sum()
total_units = filtered["units_sold"].sum()
avg_margin = (total_profit / total_revenue * 100) if total_revenue else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"£{total_revenue:,.0f}")
k2.metric("Total Profit", f"£{total_profit:,.0f}")
k3.metric("Units Sold", f"{total_units:,.0f}")
k4.metric("Avg Margin", f"{avg_margin:.1f}%")

# ── Revenue Trend ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Revenue Trend by Region")

trend = (
    filtered.groupby(["date", "region"], as_index=False)["revenue"]
    .sum()
    .sort_values("date")
)

fig_trend = px.line(
    trend,
    x="date",
    y="revenue",
    color="region",
    markers=True,
    labels={"revenue": "Revenue (£)", "date": "Month", "region": "Region"},
    template="plotly_white",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig_trend.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    yaxis_tickformat=",.0f",
    margin=dict(l=0, r=0, t=40, b=0),
)
st.plotly_chart(fig_trend, use_container_width=True)

# ── Product Category Breakdown ──────────────────────────────────────────────────
st.markdown("### Revenue by Product Category")

col_a, col_b = st.columns(2)

with col_a:
    cat_rev = filtered.groupby("product_category", as_index=False)["revenue"].sum()
    fig_pie = px.pie(
        cat_rev,
        names="product_category",
        values="revenue",
        hole=0.45,
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_pie.update_traces(textinfo="percent+label")
    fig_pie.update_layout(margin=dict(l=0, r=0, t=20, b=0), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_b:
    cat_month = (
        filtered.groupby(["month", "date", "product_category"], as_index=False)[
            "revenue"
        ]
        .sum()
        .sort_values("date")
    )
    fig_bar = px.bar(
        cat_month,
        x="month",
        y="revenue",
        color="product_category",
        barmode="stack",
        template="plotly_white",
        labels={
            "revenue": "Revenue (£)",
            "month": "Month",
            "product_category": "Category",
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_bar.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_tickformat=",.0f",
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Margin Analysis ─────────────────────────────────────────────────────────────
st.markdown("### Profit Margin Analysis")

margin_data = (
    filtered.groupby(["region", "product_category"], as_index=False)
    .agg({"revenue": "sum", "profit": "sum"})
)
margin_data["margin_pct"] = (margin_data["profit"] / margin_data["revenue"] * 100).round(1)

fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=margin_data.pivot_table(
            index="region", columns="product_category", values="margin_pct"
        ).values,
        x=sorted(margin_data["product_category"].unique()),
        y=sorted(margin_data["region"].unique()),
        colorscale="Blues",
        text=margin_data.pivot_table(
            index="region", columns="product_category", values="margin_pct"
        ).values,
        texttemplate="%{text:.1f}%",
        hovertemplate="Region: %{y}<br>Category: %{x}<br>Margin: %{z:.1f}%<extra></extra>",
    )
)
fig_heatmap.update_layout(
    template="plotly_white",
    margin=dict(l=0, r=0, t=20, b=0),
    height=350,
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ── Channel Performance ─────────────────────────────────────────────────────────
st.markdown("### Channel Performance")

channel_data = (
    filtered.groupby("channel", as_index=False)
    .agg({"revenue": "sum", "units_sold": "sum", "profit": "sum"})
)

col_c1, col_c2 = st.columns(2)

with col_c1:
    fig_channel = px.bar(
        channel_data,
        x="channel",
        y=["revenue", "profit"],
        barmode="group",
        template="plotly_white",
        labels={"value": "Amount (£)", "channel": "Channel"},
        color_discrete_sequence=["#0071e3", "#34c759"],
    )
    fig_channel.update_layout(
        legend_title_text="Metric",
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis_tickformat=",.0f",
    )
    st.plotly_chart(fig_channel, use_container_width=True)

with col_c2:
    fig_units = px.bar(
        channel_data,
        x="channel",
        y="units_sold",
        template="plotly_white",
        labels={"units_sold": "Units Sold", "channel": "Channel"},
        color_discrete_sequence=["#0071e3"],
    )
    fig_units.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis_tickformat=",.0f",
    )
    st.plotly_chart(fig_units, use_container_width=True)

# ── Raw Data Explorer ───────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("Explore Raw Data"):
    st.dataframe(
        filtered.drop(columns=["month"]).sort_values("date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download Filtered Data as CSV",
        data=filtered.to_csv(index=False),
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )


