import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer & Job Matcher")

st.info("Upload your resume and paste job description to analyze match.")

@st.cache_resource
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if resume_file and job_desc:
        with st.spinner("Loading AI model..."):
            model = load_model()

        from sentence_transformers import util

        resume_text = extract_text_from_pdf(resume_file)

        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        job_embedding = model.encode(job_desc, convert_to_tensor=True)

        score = util.cos_sim(resume_embedding, job_embedding).item() * 100

        st.success(f"✅ Match Score: {round(score, 2)}%")

        if score < 50:
            st.warning("Resume needs improvement for this role.")
        else:
            st.info("Good match! Consider applying.")

    else:
        st.error("Please upload resume and add job description")
