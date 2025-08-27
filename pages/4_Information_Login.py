import streamlit as st

st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem; 
        }
        </style>
        """, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Enter your info</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Please provide all the details below accurately to proceed.</p>", unsafe_allow_html=True)

with st.form(key="details"):
    positions=st.multiselect("Select your preferred job positions", options=["Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Scientist", "DevOps Engineer", "Mobile App Developer", "AI/ML Engineer", "Cloud Engineer"])
    skills=st.text_area("List your tech stack (comma separated)")
    if st.form_submit_button("Submit"):
        st.switch_page("pages/5_Chat.py")