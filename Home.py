import streamlit as st

st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem; 
        }
        </style>
        """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Welcome to TalentScout!</h1>", unsafe_allow_html=True)

st.divider()
st.markdown("""
##### Our intelligent hiring assistant is here to guide you through the first step of your application process. The conversation is designed to be quick, straightforward, and focused on what really matters. YOUR SKILLS.

##### **How it works:**

#####  **Introduce Yourself:** Fill in the form with the basic required details.
#####  **Share Your Expertise:** Tell us about your tech stack (languages, frameworks, tools).
#####  **Showcase Your Knowledge:** Answer a few technical questions tailored specifically to your skills.
#####  **Get a comprehensive report:** You will get a complete report based on your interview to know your strengths and weaknesses.
##### This entire process should only take a few minutes. Once completed, our human recruitment team will review your profile and be in touch about the next steps.
""")
st.divider()
st.markdown("<p style='text-align: center;'><b>CLICK HERE TO START!<b></p>", unsafe_allow_html=True)
with st.container(horizontal_alignment="center"):
    if st.button("**Start Now**", key="signup_button"):
        st.switch_page("pages/1_Information_Signup.py")
