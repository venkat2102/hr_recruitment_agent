import spacy

from pypdf import PdfReader

import io 

try :
    nlp = spacy.load("en_core_web_sm")
except OSError :
    print("Downloading spacy model")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm") 

def parse_resume_pdf_agent(pdf_file) :
    try : 
        reader = PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in reader.pages :
            text += page.extract_text() or ""
        
        return text 
    except Exception as e :
        return f"Error extracing text: {e}"

def parse_resume_txt_agent(txt_file) :
    return txt_file.getvalue().decode("utf-8")

def extract_skills_agent(text) :
    skills_list = [
        "python","r","sql","pandas","numpy","scikit_learn",
        "tableau","power bi","statistics" , "data cleaning" , "java",
        "machine learning" , "nlp" , "flask" ,"django", "fastapi","git",
        "docker", "blockchain" ,"web development" , "backend",
        "data analysis" , "predictive modeling"
    ]
    doc = nlp(text.lower())
    found_skills = {token.text for token in doc if token.text in skills_list}
    return found_skills

def get_candidate_name_agent(resume_text) :
    lines = resume_text.strip().split('\n')
    if lines :
        return lines[0].strip()
    return "unknown Candidate"

def calculate_score_agent(resume_skills,job_skills) :
    if not job_skills :
        return 0.0 
    matching_skills = resume_skills.intersection(job_skills)
    score = (len(matching_skills)/ len(job_skills)) * 100 
    return round(score , 2 )