import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("#### Aaron Adekoya")
        st.caption("Data Engineer · London, UK")
        st.divider()
        st.markdown("[LinkedIn](https://www.linkedin.com/in/aachad)")
        if st.checkbox("Show contact details", key="sidebar_contact"):
            st.markdown("aaronadek@outlook.com  \n07775 635961")
        st.divider()
