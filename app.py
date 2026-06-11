st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:
    resume_text = extract_resume_text(uploaded_file)

    st.write(resume_text[:500])