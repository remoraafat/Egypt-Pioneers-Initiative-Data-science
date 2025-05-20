# resume_analyzer.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from resume_parser import extract_text_from_pdf

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "qwen/qwen3-1.7b:free"
# MODEL = "deepseek/deepseek-prover-v2:free"

def analyze_resume(resume_text, job_description=None):
    if job_description:
        prompt = f"""
You are a professional HR recruiter evaluating a resume **specifically** for the job described below.

Your task is to:
1. Suggest 1–3 job titles the candidate could apply for, based on this resume and job description.
2. Score the resume from 0 to 100 based on how well it matches the job description, in terms of qualifications, skills, and clarity.
3. Provide 3–5 specific suggestions to improve the resume for this job.

Job Description:
\"\"\"
{job_description}
\"\"\"

Resume:
\"\"\"
{resume_text}
\"\"\"

Respond in this JSON format only:

{{
    "Name": "Candidate Name" if available,
    "Email": "Candidate Email" if available,
    "Phone": "Candidate Phone" if available,
    "LinkedIn": "Candidate LinkedIn" if available(it could be a link),
    "GitHub": "Candidate GitHub" if available (it could be a link),
    "job_titles": [ ... ],
    "score": ...,
    "experience": "Candidate Experience" if available,
    "education": "Candidate Education" if available,
    "skills": "Candidate Skills" if available,
    "certifications": "Candidate Certifications" if available,
    "suggestions": [ ... ]
}}

Don't include any extra text like ```json or markdown wrappers.
"""
    else:
        prompt = f"""
You are a professional HR recruiter. You are reviewing a resume provided below.
Your task is to:
1. Suggest 1–3 suitable job titles for the candidate.
2. Score the resume from 0 to 100 based on quality, clarity, and relevance.
3. Provide 3–5 specific suggestions to improve the resume.

Resume:
\"\"\"
{resume_text}
\"\"\"

Respond in this JSON format only:

{{
    "Name": "Candidate Name" if available,
    "Email": "Candidate Email" if available,
    "Phone": "Candidate Phone" if available,
    "LinkedIn": "Candidate LinkedIn" if available(it could be a link),
    "GitHub": "Candidate GitHub" if available (it could be a link),
    "job_titles": [ ... ],
    "score": ...,
    "experience": "Candidate Experience" if available,
    "education": "Candidate Education" if available,
    "skills": "Candidate Skills" if available,
    "certifications": "Candidate Certifications" if available,
    "suggestions": [ ... ]
}}

Don't include any extra text like ```json or markdown wrappers.
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    resume_text = extract_text_from_pdf("test.pdf")
    job_desc = extract_text_from_pdf("job_descriptions.pdf") 
    result = analyze_resume(resume_text, job_desc)
    print(result)
