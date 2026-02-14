import streamlit as st

from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_extractor import extract_skills
from utils.similarity import calculate_similarity

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🔍 AI Resume Analyzer & Job Match Dashboard")

resume  = st.sidebar.file_uploader("Upload file" , type = "pdf")
jd  = st.sidebar.text_area("Paste Job description")

if resume and jd:

    status = st.empty()
    status.info("ANALYSING RESUME...")

    resume_text     = extract_text_from_pdf(resume)
    cleaned_resume  = clean_text(resume_text)
    cleaned_jd      = clean_text(jd)

    resume_skills = extract_skills(cleaned_resume) 
    jd_skills     = extract_skills(cleaned_jd)


    match_score = calculate_similarity(cleaned_resume, cleaned_jd)

    missing_skills = list(set(jd_skills) - set(resume_skills))

    status.success("Analysis completed...")

    col1, col2, col3 = st.columns(3)

    col1.metric("Skill Match %", f"{match_score}%")
    col2.metric("Resume Skills", len(resume_skills))
    col3.metric("Missing Skills", len(missing_skills))

    st.progress(match_score / 100)

    with st.expander("📌 Resume Skills"):
        st.write(resume_skills)

    with st.expander("❌ Missing Skills"):
        st.warning(missing_skills)

    with st.expander("🧠 Improvement Suggestions"):
        if missing_skills:
            st.write("Consider adding or learning:")
            for skill in missing_skills:
                st.write(f"- {skill}")
        else:
            st.success("Your resume matches the job very well!")

else:
    st.info("Please upload a resume and enter a job description.")

