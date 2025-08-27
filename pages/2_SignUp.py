import streamlit as st
st.page_link("pages/3_Information_Signup.py")
st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Sign up</h1>", unsafe_allow_html=True)

with st.form(key="signup"):
    email= st.text_input("Enter your email")
    password= st.text_input("Enter your password", type="password")
    confirm= st.text_input("Confirm your password", type="password")
    if st.form_submit_button("Submit"):
        if password!= confirm:
            st.error("Passwords do not match. Please try again.")
        elif len(password) < 8:
            st.error("Password must be at least 8 characters long.")
        else:
            st.success("Sign up successful! Please proceed to the information page.")
            st.session_state['email']= email
            st.session_state['password']= password
            st.switch_page("pages/3_Information_Signup.py")