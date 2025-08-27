import streamlit as st
st.page_link("pages/4_Information_Login.py")
st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)

with st.form(key="login"):
    email= st.text_input("Enter your email")
    password= st.text_input("Enter your password", type="password")
    if st.form_submit_button("Submit"):
        # if 'email' in st.session_state and 'password' in st.session_state:
        #     # if email == st.session_state['email'] and password == st.session_state['password']:
        #     #     st.success("Login successful! Please proceed to the information page.")
                st.switch_page("pages/4_Information_Login.py")
            # else:
            #     st.error("Invalid email or password. Please try again.")
        # else:
        #     st.error("No account found. Please sign up first.")