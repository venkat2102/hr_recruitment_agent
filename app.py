import streamlit as st
import pandas as pd 

from test_inference import (
    parse_resume_pdf_agent,
    parse_resume_txt_agent,
    extract_skills_agent,
    calculate_score_agent,
    get_candidate_name_agent
)
st.set_page_config (
    page_title= "Recruitment AI Agent",
    page_icon = "",
    layout = "centered"
)
st.title("Recruitment AI Agent")
st.subheader("Automate Resumee Screenig with AI")

job_description = st.text_area(
    "paste the job Description Here : ",
    height = 200 , 
    placeholder = "e.g. , We are looking for a Pyhton deveeloper with skils in NLP , machine learing "
)

upload_resumes = st.file_uploader(
    "Upload Resume (.pdf or .txt)",
    type = ["pdf","txt"],
    accept_multiple_files = True
)

if st.button("screen Candidate",use_container_width=True) :
    if job_description and upload_resumes :
        with st.spinner("Screening candidates..."):
            job_skills = extract_skills_agent(job_description)
            candidate_results = []
            for resume_file in upload_resumes :
                file_extension = resume_file.name.split('.')[-1].lower()
                if file_extension == "pdf" :
                    resume_text = parse_resume_pdf_agent(resume_file)
                elif file_extension == "txt" :
                    resume_text = parse_resume_txt_agent(resume_file)
                else:
                    st.warning(f"Skipping unsupported file type : {resume_file.name}")
                    continue
                resume_skills = extract_skills_agent(resume_text)
                score = calculate_score_agent(resume_skills,job_skills)
                candidate_results.append({
                    "candidate Name" : get_candidate_name_agent(resume_text),
                    "Match score" : score ,
                    "File Name" : resume_file.name,
                    "Matching Skills" : ", ".join(resume_skills.intersection(job_skills)),

                })
        candidate_results.sort(key=lambda x:x['Match score'],reverse=True)
        st.success("screenig Complete!")
        st.markdown("----")
        st.header("Ranking of Candiadate")
        df = pd.DataFrame(candidate_results)
        st.dataframe(df,use_container_width=True)
        st.markdown("----")
        st.header("Detailed Analysis")
        for candidate in candidate_results :
            st.subheader(f"Analysis for {candidate['candidate Name']}")
            st.metric("Match Score",f"{candidate['Match score']}%")
            st.markdown("*Matching Skills:*")
            if candidate['Matching Skills']:
                st.code(candidate['Matching Skills'])
            else :
                st.warning("No skills Match")
    else :
        st.warning("please provide a job description and upload at least one resume.")