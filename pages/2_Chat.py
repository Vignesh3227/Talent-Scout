import streamlit as st
import time
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



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
    repo_id="Qwen/Qwen3-30B-A3B-Instruct-2507",
    max_new_tokens=512,
    temperature=0.1,
    provider="auto"
)
chat_model = ChatHuggingFace(llm=llm)

prompt_template = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
])
chain = prompt_template | chat_model

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.interview_state = "IN_PROGRESS"
    
    template = f'''You are a friendly but professional AI talent scout named Alex. Your goal is to conduct a technical interview for the company PGAGI.

**Your Instructions:**
1.  **Role:** You are an interviewer. Keep your questions strictly focused on the candidate's technical skills.
2.  **Process:** Ask technical questions one by one. Wait for the user's response before asking the next question.
3.  **Scoring:** Internally, keep track of the user's performance. You don't need to show a score.
4.  **Conclusion:** After 5-7 questions, conclude the interview. Start your final message with the exact phrase: "Thank you for your time. This concludes our interview." This is a critical instruction.

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

if prompt := st.chat_input("Type your response here...", disabled=(st.session_state.interview_state == "CONCLUDED")):
    user_message = HumanMessage(content=prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Analyzing..."):
        last_ai_question = ""
        for msg in reversed(st.session_state.history):
            if isinstance(msg, AIMessage):
                last_ai_question = msg.content
                break

        guardrail_prompt_content = f"""
You are an interview moderator AI. Your only job is to classify a user's response.
The interviewer asked: '{last_ai_question}'
The user responded: '{prompt}'

Is the user's response on-topic or off-topic?
- An on-topic response attempts to answer the question or asks for a hint or says I dont know.
- An off-topic response changes the subject or asks an unrelated question.

Your response MUST be a single word: either ON_TOPIC or OFF_TOPIC. Do not add any explanation or punctuation.
"""
        guardrail_message = SystemMessage(content=guardrail_prompt_content)
        guardrail_response = chat_model.invoke([guardrail_message])
        
        moderator_decision = guardrail_response.content.strip().upper()

    if "ON_TOPIC" in moderator_decision:
        st.session_state.history.append(user_message)
        with st.chat_message("ai"):
            with st.spinner("Thinking..."):
                ai_response = chain.invoke({"history": st.session_state.history})
                st.markdown(ai_response.content)
        
        st.session_state.history.append(ai_response)
        
        if "This concludes our interview" in ai_response.content:
            st.session_state.interview_state = "CONCLUDED"
            st.success("Interview complete! Redirecting to the results page...")
            time.sleep(8) 
            st.switch_page("pages/3_Result.py")

    else: 
        with st.chat_message("ai"):
            canned_response = "That's an interesting point, but let's please stay focused on the technical questions. Could you tell me about the last question I asked?"
            st.markdown(canned_response)