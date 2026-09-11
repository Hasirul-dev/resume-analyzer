from flask import Flask, render_template, request
import fitz

app = Flask(__name__)

skills = [
    "python",
    "java",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "flask",
    "machine learning",
    "data science",
    "django",
    "git",
    "github"
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]
    job_description = request.form["job_description"]

    # Read PDF
    pdf = fitz.open(
        stream=resume.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    # Convert to lowercase
    resume_text = text.lower()
    job_text = job_description.lower()

    # Find resume skills
    resume_skills = []

    for skill in skills:
        if skill in resume_text:
            resume_skills.append(skill)

    # Find required job skills
    job_skills = []

    for skill in skills:
        if skill in job_text:
            job_skills.append(skill)

    # Find matching skills
    matched_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)

    # Find missing skills
    missing_skills = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)

    #suggestions
    suggestions = []

    for skill in missing_skills:
       suggestions.append(
          f"Consider adding{skills} to your resume."
       )

    # Calculate match percentage
    if len(job_skills) > 0:
        score = (len(matched_skills) / len(job_skills)) * 100
    else:
        score = 0

    # Basic ATS Score
    ats_score = 0

    if len(text) > 200:
      ats_score += 25

      if len(resume_skills) >= 3:
       ats_score += 25

    if "education" in resume_text:
      ats_score += 15

      if "experience" in resume_text:
       ats_score += 15

       if "project" in resume_text:
         ats_score += 10

      if "contact" in resume_text or "email" in resume_text:
       ats_score += 10     




    return render_template (
    "result.html",
    score=score,
    ats_score=ats_score,
    matched_skills=matched_skills,
    missing_skills=missing_skills,
    resume_skills=resume_skills,
    suggestions = suggestions
)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)