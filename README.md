# TalentScout

## Overview

TalentScout is a web application built with Streamlit that allows users to sign up, chat, and receive results based on their technical skills. The project is organized to provide an interactive evaluation experience, leveraging Python and several data science and web libraries.

Link to use the app https://talent-sc0ut.streamlit.app/

## Features

- **Information Signup Page**: A simple form that collects user data for evaluation.
- **Chat Interface**: Interactive chat for technical Q&A or skill assessment.
- **Result Page**: Displays evaluation results and feedback.
- **Streamlit UI**: Modern, responsive web interface using Streamlit.

## Project Structure

```
Home.py                  # Main entry point for the Streamlit app
requirements.txt         # Python dependencies
agent/                   # Python virtual environment and dependencies
pages/
  1_Information_Signup.py  # Signup page logic
  2_Chat.py                # Chat interface logic
  3_Result.py              # Result display logic
.streamlit/
  config.toml  # custom theme
  secrets.toml # add your huggingface API key here
```

## Setup Instructions

1. **Clone the repository**
   ```powershell
   git clone <repo-url>
   cd "Talent Scout"
   ```
2. **Create and activate a virtual environment**
   (If not already present)
   ```powershell
   python -m venv agent
   .\agent\Scripts\Activate.ps1
   ```
3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run the application**
   ```powershell
   streamlit run Home.py
   ```

## Usage

- Access the app in your browser at the provided local URL after running the Streamlit command.
- Navigate through the signup, chat, and result pages using the sidebar or navigation buttons.

## Dependencies

All required Python packages are listed in `requirements.txt`. Key libraries include:
- streamlit
- numpy
- pandas
- plotly
- langchain
- huggingface
- and others for data processing and visualization

