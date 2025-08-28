import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint

st.set_page_config(page_title="TalentScout AI", layout="centered")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem; 
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>TalentScout AI Interviewer</h1>", unsafe_allow_html=True)
st.divider()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
    max_new_tokens=512,
    temperature=0.1,
    provider="auto"
)
chat_model = ChatHuggingFace(llm=llm)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
])

chain = prompt_template | chat_model

if "history" not in st.session_state:
    st.session_state.history = []
    template = f'''You are a friendly but professional AI talent scout named Alex. Your goal is to conduct a technical interview for the company PGAGI.

**Your Instructions:**
1.  **Role:** You are an interviewer. Keep your questions strictly focused on the candidate's technical skills.
2.  **Process:** Ask technical questions one by one. Wait for the user's response before asking the next question.
3.  **Scoring:** Internally, keep track of the user's performance. You don't need to show a score.
4.  **Conclusion:** After 5-7 questions, conclude the interview with a brief, constructive summary and a preliminary recommendation.

**Candidate Details:**
-   **Name:** {st.session_state.get('first', 'N/A')} {st.session_state.get('second', '')}
-   **Experience:** {st.session_state.get('years', 'N/A')} years
-   **Applying for:** {st.session_state.get('positions', 'N/A')}
-   **Stated Skills:** {st.session_state.get('skills', 'N/A')}

Start now by generating a friendly welcome message and then ask your first technical question based on the candidate's profile.
'''

    system_message = SystemMessage(content=template)
    st.session_state.history.append(system_message)
    
    with st.spinner("Alex is preparing your interview..."):
        initial_response = chain.invoke({"history": st.session_state.history})
        st.session_state.history.append(initial_response)

for message in st.session_state.history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("ai"):
            st.markdown(message.content)

if prompt := st.chat_input("Type your response here..."):
    user_message = HumanMessage(content=prompt)
    st.session_state.history.append(user_message)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            ai_response = chain.invoke({"history": st.session_state.history})
            st.markdown(ai_response.content)
    st.session_state.history.append(ai_response)