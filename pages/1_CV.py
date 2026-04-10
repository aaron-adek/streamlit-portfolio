import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from sidebar import render_sidebar

st.set_page_config(page_title="CV | Aaron Adekoya", page_icon="A", layout="wide")
render_sidebar()

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0071e3;
        border-bottom: 2px solid #0071e3;
        padding-bottom: 6px;
        margin-top: 28px;
        margin-bottom: 12px;
    }
    .job-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1d1d1f;
    }
    .job-company {
        font-size: 1rem;
        color: #0071e3;
        font-weight: 600;
    }
    .job-date {
        font-size: 0.9rem;
        color: #6e6e73;
        font-style: italic;
    }
    .skill-badge {
        display: inline-block;
        background: #0071e3;
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        margin: 4px 4px;
        font-size: 0.85rem;
    }
    .skill-badge-secondary {
        display: inline-block;
        background: #f5f5f7;
        color: #1d1d1f;
        padding: 4px 14px;
        border-radius: 20px;
        margin: 4px 4px;
        font-size: 0.85rem;
        border: 1px solid #d2d2d7;
    }
    .cert-card {
        background: #f5f5f7;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ──────────────────────────────────────────────────────────────────────
st.title("Curriculum Vitae")

st.markdown(
    """
    **Aaron Adekoya** · Data Engineer · London, United Kingdom  
    [LinkedIn](https://www.linkedin.com/in/aachad)
    """
)
if st.checkbox("Show contact details", key="cv_contact"):
    st.markdown("📧 aaronadek@outlook.com · 📱 07775 635961")

# ── Summary ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Summary</div>', unsafe_allow_html=True)
st.markdown(
    """
    Data Engineer with **5+ years** of experience building and scaling cloud data platforms
    on **AWS** and **Azure**. Skilled in developing high-volume, reliable data products and
    taking **LLM-based systems** from idea to production. Known for quickly picking up new
    technologies and delivering reliable solutions that drive measurable business impact.
    """
)

# ── Core Skills ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Core Skills</div>', unsafe_allow_html=True)

core_skills = [
    "Cloud Architectures (AWS/Azure)",
    "ETL / ELT Pipeline Design",
    "API Integration",
    "LLM Services & Data Integration",
    "Data Security & Governance",
    "Distributed Data Processing (Spark, EMR)",
    "Infrastructure as Code",
    "CI/CD",
    "Data Modelling",
]

badges_html = " ".join(
    f'<span class="skill-badge">{skill}</span>' for skill in core_skills
)
st.markdown(badges_html, unsafe_allow_html=True)

# ── Tools & Technology ──────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">Tools & Technology</div>', unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Languages**")
    lang_badges = " ".join(
        f'<span class="skill-badge-secondary">{t}</span>'
        for t in ["Python", "PySpark", "SQL"]
    )
    st.markdown(lang_badges, unsafe_allow_html=True)

    st.markdown("**Cloud – AWS**")
    aws_badges = " ".join(
        f'<span class="skill-badge-secondary">{t}</span>'
        for t in ["S3", "EC2", "EKS", "EMR", "Airflow", "Bedrock"]
    )
    st.markdown(aws_badges, unsafe_allow_html=True)

    st.markdown("**Cloud – Azure**")
    azure_badges = " ".join(
        f'<span class="skill-badge-secondary">{t}</span>'
        for t in ["Azure Data Factory", "Data Lake", "SQL Managed Instance"]
    )
    st.markdown(azure_badges, unsafe_allow_html=True)

with col2:
    st.markdown("**Data Platforms**")
    dp_badges = " ".join(
        f'<span class="skill-badge-secondary">{t}</span>'
        for t in ["Snowflake", "Databricks", "Power BI"]
    )
    st.markdown(dp_badges, unsafe_allow_html=True)

    st.markdown("**DevOps**")
    devops_badges = " ".join(
        f'<span class="skill-badge-secondary">{t}</span>'
        for t in ["Jenkins", "Kubernetes", "Terraform"]
    )
    st.markdown(devops_badges, unsafe_allow_html=True)

# ── Professional Experience ─────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">Professional Experience</div>',
    unsafe_allow_html=True,
)

# -- Amex GBT --
st.markdown(
    """
    <span class="job-company">American Express Global Business Travel</span>
    <span class="job-date"> · Aug 2024 to Present</span><br>
    <span class="job-title">Data Engineer (AWS Stack)</span>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    - Led the design and productionisation of an **AI-driven incident resolution system**,
      reducing resolution time by **~20%**, awarded **Leadership Recognition Award** for AI innovation
    - Architected and drove the implementation of **secure, enterprise-scale ETL pipelines**
      handling high-volume (billions of rows) production data through structured data models
    - Delivered **LLM cost tracking and optimization** strategy via Terraform-managed Bedrock inference profiles
    - Streamlined Jenkins CI/CD pipelines, **reducing average deployment times by 55%** and reducing release friction
    - Implemented **data security controls** including encryption, access policies, and data retention strategies
      to ensure compliance and protect sensitive data
    """
)

with st.expander("Key Project: Aladdin Service", expanded=True):
    st.markdown(
        """
        - Owned the design and delivery of a **Kubernetes-based AI service** using Amazon Bedrock (LLMs),
          Playwright MCP and FastAPI
        - Partnered with customer journey analytics stakeholders to build **API-driven workflows**
          to simulate user behaviour (login, navigation, tag validation) across web applications
        - **Automated detection** of broken Adobe Analytics tags, replacing manual QA processes
        - Drove operational efficiency, reducing manual validation workload on analysts
          from **36 to 24 analyst-weeks** with reductions still happening
        - Improved data reliability and **trust in analytics**, reducing downstream reporting issues
        """
    )

st.markdown("---")

# -- LexisNexis --
st.markdown(
    """
    <span class="job-company">LexisNexis Risk Solutions Group</span>
    <span class="job-date"> · Sep 2020 to Mar 2024</span><br>
    <span class="job-title">Analytics Engineer (Microsoft Azure Stack)</span>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    - Multiple corporate awards for **Individual Excellence**, **Delivering Business Value** and **Innovation**
    - Redesigned Salesforce ingestion pipelines, **reducing runtime by 74%**
    - Led the design and delivery of cross-system **Customer360 data platform** and financial forecasting dashboard, integrating multiple
      upstream sources into a **unified data model** enabling consistent reporting and decision-making
      from a single source of truth
    - **Mentor** for the graduate technology program and providing training and onboarding
      to Junior Engineers/Analysts
    """
)

# ── Education & Certifications ──────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">Education & Certifications</div>',
    unsafe_allow_html=True,
)

st.markdown("#### University of Southampton")
st.markdown("Aerospace Engineering, Bachelor of Engineering *(Graduated 2019)*")

st.markdown("#### Certifications")

certs = [
    ("Databricks Certified Data Engineer Associate", "Issued Mar 2024 · Expired Mar 2026"),
    ("Azure Data Engineer Associate", "Issued Jun 2021 · Expired Jun 2025"),
    (
        "Financial Modelling and Valuation Analyst",
        "Corporate Finance Institute · Issued Aug 2020",
    ),
]

for cert_name, cert_detail in certs:
    st.markdown(
        f"""
        <div class="cert-card">
            <strong>{cert_name}</strong><br>
            <span style="color:#6e6e73; font-size:0.85rem;">{cert_detail}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


