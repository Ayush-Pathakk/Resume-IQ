import os
import tempfile
import streamlit as st
from core import clean, process_resume

st.set_page_config(page_title="ResumeIQ", layout="centered")
st.title("ResumeIQ — Resume Screener")

jd = st.text_area("Job Description", height=200, placeholder="Paste the job description here...")
uploaded = st.file_uploader("Upload Resumes (PDF)", type="pdf", accept_multiple_files=True)

if st.button("Screen Resumes") and jd and uploaded:
    jd_clean = clean(jd)
    results = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for f in uploaded:
            path = os.path.join(tmpdir, f.name)
            with open(path, "wb") as out:
                out.write(f.read())
            results.append(process_resume(path, jd_clean, f.name))

    results.sort(key=lambda r: r.score, reverse=True)

    st.markdown("---")
    st.subheader("Results")

    for r in results:
        if r.error:
            st.error(f"{r.filename}: {r.error}")
            continue
        color = "green" if r.score >= 60 else "orange" if r.score >= 40 else "red"
        st.markdown(f"**{r.filename}**")
        st.progress(int(r.score))
        st.markdown(f"Score: <span style='color:{color}'><b>{r.score}%</b></span>", unsafe_allow_html=True)
        st.caption("Matched Skills: " + (", ".join(r.matched_skills) if r.matched_skills else "None"))
        st.markdown("---")
