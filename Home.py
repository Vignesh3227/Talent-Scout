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

#####  **Introduce Yourself:** The chatbot will ask for some basic information to get to know you.
#####  **Share Your Expertise:** Tell us about your tech stack (languages, frameworks, tools).
#####  **Showcase Your Knowledge:** Answer a few technical questions tailored specifically to your skills.

##### This entire process should only take a few minutes. Once completed, our human recruitment team will review your profile and be in touch about the next steps.
""")
st.divider()
signup, login= st.columns(2, gap="medium")

with signup:
    st.write("**New here? Sign up to get started!**")
    if st.button("**Sign Up**", key="signup_button"):
        st.switch_page("pages/2_SignUp.py")
with login:
    st.write("**Already have an account? Log in to continue!**")
    if st.button("**Log In**", key="login_button"):
        st.switch_page("pages/1_Login.py")