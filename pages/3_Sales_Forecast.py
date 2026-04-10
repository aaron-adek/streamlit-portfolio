import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score
from sidebar import render_sidebar

st.set_page_config(page_title="Sales Forecast | Aaron Adekoya", page_icon="A", layout="wide")
render_sidebar()

# ── Load data ───────────────────────────────────────────────────────────────────
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sales_data.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df["profit"] = df["revenue"] - df["cost"]
    df["month_num"] = (
        (df["date"].dt.year - df["date"].dt.year.min()) * 12
        + df["date"].dt.month
    )
    return df


df = load_data()

# ── Page header ─────────────────────────────────────────────────────────────────
st.title("Sales Forecasting")
st.markdown(
    """
    This page walks through a lightweight forecasting pipeline — from
    raw data to predictions you can interact with. Pick a region and
    category below to see how the model performs and generate forward-looking
    revenue estimates.
    """
)

st.divider()
st.markdown("### Pipeline Overview")
st.markdown(
    """
    1. **Extract** — Ingest raw data from CSV, API, or database  \n
    2. **Transform** — Feature engineering, encoding, aggregation  \n
    3. **Model** — Train and cross-validate  \n
    4. **Serve** — Interactive predictions via this app
    """
)

# ── Section 2: Feature Engineering ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### Feature Engineering")

st.markdown(
    """
    Converting raw data into model-ready features:
    - **Categorical encoding**: Region and product category converted to numeric features via Label Encoding
    - **Time features**: Month number extracted as a trend indicator
    - **Derived metrics**: Profit, margin percentage computed from raw columns
    """
)


@st.cache_data
def prepare_features(data: pd.DataFrame):
    le_region = LabelEncoder()
    le_category = LabelEncoder()
    le_channel = LabelEncoder()

    features = data.copy()
    features["region_enc"] = le_region.fit_transform(features["region"])
    features["category_enc"] = le_category.fit_transform(features["product_category"])
    features["channel_enc"] = le_channel.fit_transform(features["channel"])

    feature_cols = ["month_num", "region_enc", "category_enc", "channel_enc", "units_sold"]
    X = features[feature_cols]
    y = features["revenue"]

    return X, y, le_region, le_category, le_channel, feature_cols


X, y, le_region, le_category, le_channel, feature_cols = prepare_features(df)

with st.expander("View Feature Matrix (first 10 rows)"):
    st.dataframe(
        pd.concat([X, y], axis=1).head(10),
        use_container_width=True,
        hide_index=True,
    )

# ── Section 3: Model Training & Evaluation ──────────────────────────────────────
st.markdown("---")
st.markdown("### Model Training & Evaluation")


@st.cache_data
def train_model(_X, _y):
    model = LinearRegression()
    model.fit(_X, _y)
    preds = model.predict(_X)

    cv_scores = cross_val_score(model, _X, _y, cv=5, scoring="r2")
    mae = mean_absolute_error(_y, preds)
    r2 = r2_score(_y, preds)

    return model, preds, cv_scores, mae, r2


model, preds, cv_scores, mae, r2 = train_model(X, y)

m1, m2, m3 = st.columns(3)
m1.metric("R² Score", f"{r2:.4f}")
m2.metric("Mean Absolute Error", f"£{mae:,.0f}")
m3.metric("CV R² (5-fold)", f"{cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Actual vs Predicted
st.markdown("#### Actual vs Predicted Revenue")

results_df = pd.DataFrame({"Actual": y, "Predicted": preds})
results_df["index"] = range(len(results_df))

fig_pred = go.Figure()
fig_pred.add_trace(
    go.Scatter(
        x=results_df["index"],
        y=results_df["Actual"],
        mode="markers",
        name="Actual",
        marker=dict(color="#0071e3", size=4, opacity=0.5),
    )
)
fig_pred.add_trace(
    go.Scatter(
        x=results_df["index"],
        y=results_df["Predicted"],
        mode="markers",
        name="Predicted",
        marker=dict(color="#ff6b35", size=4, opacity=0.5),
    )
)
fig_pred.update_layout(
    template="plotly_white",
    xaxis_title="Sample Index",
    yaxis_title="Revenue (£)",
    yaxis_tickformat=",.0f",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=40, b=0),
    height=400,
)
st.plotly_chart(fig_pred, use_container_width=True)

# ── Section 4: Interactive Prediction ───────────────────────────────────────────
st.markdown("---")
st.markdown("### Interactive Revenue Prediction")
st.markdown(
    "Adjust the inputs below to generate a revenue prediction for different scenarios."
)

col_i1, col_i2 = st.columns(2)

with col_i1:
    pred_region = st.selectbox("Region", options=sorted(df["region"].unique()))
    pred_category = st.selectbox(
        "Product Category", options=sorted(df["product_category"].unique())
    )
    pred_channel = st.selectbox("Channel", options=sorted(df["channel"].unique()))

with col_i2:
    pred_month = st.slider(
        "Forecast Month (months from start)",
        min_value=1,
        max_value=18,
        value=7,
        help="1 = Jan 2024, 7 = Jul 2024, etc.",
    )
    pred_units = st.number_input(
        "Expected Units Sold", min_value=100, max_value=20000, value=3000, step=100
    )

if st.button("Generate Prediction", type="primary"):
    input_features = pd.DataFrame(
        {
            "month_num": [pred_month],
            "region_enc": le_region.transform([pred_region]),
            "category_enc": le_category.transform([pred_category]),
            "channel_enc": le_channel.transform([pred_channel]),
            "units_sold": [pred_units],
        }
    )

    prediction = model.predict(input_features)[0]

    st.success(f"**Predicted Revenue: £{prediction:,.0f}**")

    # Show context
    historical_avg = df[
        (df["region"] == pred_region) & (df["product_category"] == pred_category)
    ]["revenue"].mean()

    delta = ((prediction - historical_avg) / historical_avg * 100) if historical_avg else 0

    st.markdown(
        f"""
        | Metric | Value |
        |--------|-------|
        | Historical Average (same region + category) | £{historical_avg:,.0f} |
        | Predicted Revenue | £{prediction:,.0f} |
        | Delta vs Historical | {delta:+.1f}% |
        """
    )

# ── Section 5: Data Quality Checks ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### Data Quality Checks")
st.markdown(
    """
    Automated checks that run against the dataset to catch issues early.
    """
)

checks = {
    "Check": [
        "No null values in key columns",
        "Revenue > 0 for all records",
        "Cost ≤ Revenue (valid margins)",
        "Date range is continuous (no gaps)",
        "All regions present in every month",
    ],
    "Status": [
        "✅ Pass" if df[["date", "region", "revenue", "cost"]].notnull().all().all() else "❌ Fail",
        "✅ Pass" if (df["revenue"] > 0).all() else "❌ Fail",
        "✅ Pass" if (df["cost"] <= df["revenue"]).all() else "❌ Fail",
        "✅ Pass"
        if df["date"].nunique() == len(pd.date_range(df["date"].min(), df["date"].max(), freq="MS"))
        else "❌ Fail",
        "✅ Pass"
        if all(
            set(df["region"].unique()) == set(df[df["date"] == d]["region"].unique())
            for d in df["date"].unique()
        )
        else "❌ Fail",
    ],
    "Description": [
        "Ensures no missing data in critical pipeline columns",
        "Business rule: revenue must be positive",
        "Validates cost-revenue relationship for margin calculations",
        "Checks for missing months that could skew trend analysis",
        "Confirms all EMEIA regions report each period",
    ],
}

st.dataframe(
    pd.DataFrame(checks),
    use_container_width=True,
    hide_index=True,
)


