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
    first= st.text_input("Enter your first name")
    second= st.text_input("Enter your second name")
    number=st.number_input("Enter your phone number", min_value=1000000000, max_value=9999999999, step=1)
    age=st.slider("Select your age", min_value=10, max_value=100, step=1)
    years=st.selectbox("Select your years of experience", options=["0-1", "1-3", "3-5", "5+"])
    positions=st.multiselect("Select your preferred job positions", options=["Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Scientist", "DevOps Engineer", "Mobile App Developer", "AI/ML Engineer", "Cloud Engineer"])
    skills=st.text_area("List your tech stack (comma separated)")
    if st.form_submit_button("Submit"):
        st.session_state['first']= first
        st.session_state['second']= second
        st.session_state['number']= number
        st.session_state['age']= age
        st.session_state['years']= years
        st.session_state['positions']= positions
        st.session_state['skills']= skills.strip().split(',')
        st.switch_page("pages/2_Chat.py")
