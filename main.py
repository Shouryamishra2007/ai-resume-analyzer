import streamlit as st
from pypdf import PdfReader
from groq import Groq
import os

st.title("AI Resume Analyzer")

client = Groq(
        api_key="groq_api_key"
    )

prompt = st.text_input(
    "Prompt",
    value="""
Give:
1. ATS Score
2. Missing Skills
3. Strong Points
4. Improvement Suggestions
"""
)

uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

def extract_resume_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(prompt, text):
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
    {prompt}
                resume: {text}
    """

            }
        ],
        model= "llama-3.3-70b-versatile"
    )
   
    return chat_completion
    

def save_analysis(chat_completion):
    content = chat_completion.choices[0].message.content

    with open("analysis.txt", "w", encoding="utf-8") as file:
        file.write(content)
        st.subheader("Analysis Result")
        st.markdown(content)

try:
   
   
    
    if uploaded_file:
        st.success("Resume Uploaded Successfully!!")

    if st.button("Analyze resume"):

        resume_text = extract_resume_text(uploaded_file)
        chat_completion = analyze_resume(prompt, resume_text)
        save_analysis(chat_completion)
        st.success("Analysis saved successfully")

        if uploaded_file and prompt:
        
            resume_text = extract_resume_text(uploaded_file)

            with st.spinner("Analysing resume...."):
                chat_completion = analyze_resume(
                    prompt,
                    resume_text
                )

            save_analysis(chat_completion)

            st.success("Analysis Completed!")

except Exception as e:
    print("Error:", {e})
