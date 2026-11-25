from google import genai
from pydantic import BaseModel
from typing import List


client = genai.Client()


class ResumeProfile(BaseModel):
    education: str
    projects: List[str]
    certifications: List[str]
    interests: List[str]
    career_preferences: str


def extract_resume_profile(resume_text):

    prompt = f"""
You are a resume information extraction system.

Extract ONLY information that is explicitly present in the resume below.

Do NOT invent, infer, or assume information that is not stated.

Resume:
----------------
{resume_text}
----------------

Extract the following:

1. Education / qualifications
   Include degrees, programs, universities, colleges, and relevant
   educational qualifications.

2. Projects
   List projects explicitly mentioned in the resume.

3. Certifications
   List certifications explicitly mentioned in the resume.

4. Interests
   Extract interests or areas of interest ONLY if explicitly stated
   in the resume.

5. Career preferences
   Extract career preferences ONLY if explicitly stated in the resume,
   such as preferred roles, industries, work areas, or career objectives.

IMPORTANT:

- If a category is not present in the resume, return an empty value.
- Do not convert skills into interests.
- Do not assume a career preference from a degree.
- Do not assume a project from a skill.
- Do not invent certifications.
- Preserve the meaning of the original resume.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ResumeProfile,
            },
        )

        return ResumeProfile.model_validate_json(response.text)

    except Exception as e:

        print("❌ Resume parser error:", repr(e))
        return None