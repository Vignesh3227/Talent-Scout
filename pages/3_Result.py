import streamlit as st
import pandas as pd
import plotly.express as px
import json
from langchain_core.messages import SystemMessage
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint

st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem; 
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Interview Results</h1>", unsafe_allow_html=True)
st.divider()


try:
    llm=HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
        max_new_tokens=1024, 
        temperature=0.1,
        provider="auto"
    )
    chat_model=ChatHuggingFace(llm=llm)
except Exception as e:
    st.error(f"Failed to initialize the language model. Please check your API token. Error: {e}")
    st.stop()


def generate_analysis(history):
    st.info("Analyzing the interview transcript... This may take a moment.")
    transcript="\n".join([f"{msg.type.upper()}: {msg.content}" for msg in history])

    analyzer_prompt = f"""
You are a highly experienced Senior Technical Recruiter and Talent Analyst. Your task is to analyze the following interview transcript and provide a structured, unbiased report in JSON format.

**Instructions:**
1.  Read the entire transcript carefully.
2.  Evaluate the candidate's performance based on their answers.
3.  Assess strengths and areas for improvement.
4.  Provide numerical scores (out of 10) for the specified skill categories.
5.  Give a clear final recommendation.
6. You have to be extremely strict in your grading.

**Transcript to Analyze:**
**Required JSON Output Format:**
Please provide ONLY the JSON object below with your analysis. Do not include any other text or markdown formatting.

{{
    "overall_summary": "A brief, one-paragraph summary of the candidate's performance.",
    "strengths": [
        "A key strength observed during the interview.",
        "Another positive attribute or skill demonstrated."
    ],
    "areas_for_improvement": [
        "A specific area where the candidate could improve.",
        "Another constructive piece of feedback."
    ],
    "scores": {{
        "Technical Knowledge": 0,
        "Problem-Solving": 0,
        "Communication": 0,
        "Clarity of Thought": 0
    }},
    "recommendation": "A final recommendation, e.g., 'Strongly Recommend for Next Round', 'Consider for a Junior Role', or 'Not a Fit at This Time'."
}}
"""
    
    try:
        system_message=SystemMessage(content=analyzer_prompt)
        response=chat_model.invoke([system_message])
        return response.content
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
        return None

if "history" not in st.session_state or len(st.session_state.history) <= 2:
    st.warning("The interview hasn't been completed yet. Please go to the 'Interviewer' page to start.")
    st.page_link("1_Information_Signup.py")
    st.stop()

if "analysis_report" not in st.session_state:
    with st.spinner("Compiling your report... "):
        raw_analysis = generate_analysis(st.session_state.history)

        try:
            json_start = raw_analysis.find('{')
            json_end = raw_analysis.rfind('}') + 1
            clean_json_str = raw_analysis[json_start:json_end]
            
            st.session_state.analysis_report = json.loads(clean_json_str)
        except (json.JSONDecodeError, AttributeError) as e:
            st.error(f"Failed to parse the analysis report. The AI's response might be malformed. Error: {e}")
            st.code(raw_analysis)
            st.stop()

report=st.session_state.analysis_report

candidate_name = f"{st.session_state.get('first', 'Candidate')} {st.session_state.get('second', '')}"
st.header(f"Report for: {candidate_name}")

st.subheader("Overall Summary")
st.write(report.get("overall_summary", "No summary available."))

st.subheader("Recommendation")
recommendation = report.get("recommendation", "No recommendation available.")
if "Strongly Recommend" in recommendation:
    st.success(f"**{recommendation}**")
elif "Consider" in recommendation:
    st.warning(f"**{recommendation}**")
else:
    st.error(f"**{recommendation}**")

st.subheader("Skill Assessment")

scores=report.get("scores", {})
if scores:

    df=pd.DataFrame(list(scores.items()), columns=['Skill', 'Score'])
    df['Score']=pd.to_numeric(df['Score'])

    fig=px.line_polar(df, r='Score', theta='Skill', line_close=True, 
                        range_r=[0, 10],
                        title="Candidate Skill Radar")
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No skill scores were provided in the analysis.")


st.subheader("👍 Strengths & 👎 Areas for Improvement")
col1, col2=st.columns(2)

with col1:
    st.markdown("##### Strengths")
    strengths=report.get("strengths", [])
    for strength in strengths:
        st.markdown(f"- {strength}")

with col2:
    st.markdown("##### Areas for Improvement")
    improvements=report.get("areas_for_improvement", [])
    for improvement in improvements:
        st.markdown(f"- {improvement}")

with st.expander("Show Full Interview Transcript"):
    for msg in st.session_state.history:
        if msg.type== 'human':
            st.markdown(f"**You:** {msg.content}")
        elif msg.type== 'ai':
            if "You are a friendly but professional AI talent scout" not in msg.content:
                st.markdown(f"**Alex (AI):** {msg.content}")