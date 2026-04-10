import streamlit as st

from sidebar import render_sidebar

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

render_sidebar()

st.markdown("# Aaron Adekoya")
st.markdown("Data Engineer · London, UK")

st.markdown(
    """
    Data Engineer with 5+ years of experience building cloud data platforms
    on AWS and Azure. I work on high-volume data products, ETL pipelines, and
    have taken LLM-based systems from prototype to production.
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

st.markdown("### Core Skills")

fit_data = {
    "Skill": [
        "Streamlit web applications",
        "Python",
        "SQL & data modelling",
        "Data visualisation",
        "ETL / ELT pipeline design",
        "Cloud platforms (AWS, Azure)",
        "Financial / commercial datasets",
        "Data quality & governance",
        "Continuous integration & deployment",
        "Collaboration & communication",
    ],
    "Experience": [
        "This app is a working example",
        "5+ years of Python, PySpark; production FastAPI services",
        "5+ years SQL experience across Databricks, Snowflake and more",
        "3 years Power BI dashboard development with actionabile insights",
        "High-volume ETL pipelines for various internal business functions",
        "AWS (S3, EC2, EKS, EMR, Bedrock) & Azure (ADF, Data Lake)",
        "Cross-system Customer360 platform; sales finance pipelines",
        "Encryption, access policies, retention strategies for compliance",
        "Robust and streamlined CI/CD pipelines for data products",
        "Cross-functional project lead; mentored juniors; multiple awards",
    ],
}

st.dataframe(
    fit_data,
    use_container_width=True,
    hide_index=True,
)
