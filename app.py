import streamlit as st

st.set_page_config(
    page_title="Aaron Adekoya | Data Engineer",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stat-row {
        display: flex;
        gap: 32px;
        margin: 20px 0 28px 0;
    }
    .stat-item {
        text-align: center;
        flex: 1;
    }
    .stat-value {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1d1d1f;
    }
    .stat-label {
        font-size: 0.82rem;
        color: #86868b;
        margin-top: 2px;
    }
    a { color: #0071e3; }
    </style>
    """,
    unsafe_allow_html=True,
)

from sidebar import render_sidebar
render_sidebar()

st.markdown("# Aaron Adekoya")
st.markdown("Data Engineer · London, UK")

st.markdown(
    """
    I'm a Data Engineer with 5+ years of experience building cloud data platforms
    on AWS and Azure. I work on high-volume data products, ETL pipelines, and
    have taken LLM-based systems from prototype to production. This site is a
    working example of a Streamlit application.
    """
)

st.markdown(
    """
    <div class="stat-row">
        <div class="stat-item">
            <div class="stat-value">5+</div>
            <div class="stat-label">Years experience</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">~20%</div>
            <div class="stat-label">Incident resolution time reduced</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">55%</div>
            <div class="stat-label">Deployment time reduced</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">74%</div>
            <div class="stat-label">Pipeline runtime reduced</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.markdown("### Pages")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("**CV**")
    st.markdown(
        "Professional experience, skills, education, and certifications."
    )

with col_b:
    st.markdown("**Sales Analytics**")
    st.markdown(
        "Interactive dashboard with filters, KPIs, margin analysis, and trend charts."
    )

with col_c:
    st.markdown("**Sales Forecast**")
    st.markdown(
        "Revenue forecasting pipeline with model evaluation and scenario testing."
    )

st.divider()

st.markdown("### Role Alignment")

fit_data = {
    "Requirement": [
        "Streamlit web applications",
        "Python & clean code",
        "Data visualisation (Plotly, Matplotlib)",
        "ETL / ELT pipeline design",
        "Cloud platforms (AWS, Azure)",
        "Financial / commercial datasets",
        "Data quality & governance",
        "Snowflake & modern warehouses",
        "Airflow orchestration",
        "Collaboration & communication",
    ],
    "Experience": [
        "This app is a working example",
        "5+ years of Python, PySpark; production FastAPI services",
        "Plotly dashboards in this app; Power BI reporting at LexisNexis",
        "High-volume ETL pipelines (billions of rows) at Amex GBT",
        "AWS (S3, EC2, EKS, EMR, Bedrock) & Azure (ADF, Data Lake)",
        "Cross-system Customer360 platform; sales finance pipelines",
        "Encryption, access policies, retention strategies for compliance",
        "Snowflake & Databricks certified; hands-on warehouse delivery",
        "Production Airflow orchestration on AWS",
        "Cross-functional project lead; mentored juniors; multiple awards",
    ],
}

st.dataframe(
    fit_data,
    use_container_width=True,
    hide_index=True,
)
