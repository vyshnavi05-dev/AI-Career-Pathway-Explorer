# AI Assistant for Personalized Career Pathway Exploration in Universities

## Description

The AI Career Pathway Explorer is an AI-assisted web application designed to help university students identify suitable career opportunities based on their skills, proficiency levels, academic background, interests, projects, and certifications.

The system combines resume analysis, proficiency-weighted skill matching, an O*NET 31.0-derived career knowledge base, and Google Gemini AI to provide personalized career recommendations and structured career development pathways.

## Features

- **Resume Analysis:** Extracts relevant skills and profile information from uploaded PDF resumes.
- **Manual Profile Entry:** Allows students to enter and customize their academic and technical profiles.
- **Skill Proficiency Assessment:** Enables students to rate their skills on a scale of 1 to 5.
- **Personalized Career Recommendations:** Recommends the top three suitable career paths based on skill proficiency and occupational requirements.
- **Skill Gap Analysis:** Identifies existing skills and areas requiring improvement.
- **Course and Certification Suggestions:** Provides relevant learning and professional development suggestions.
- **What-If Simulation:** Allows students to simulate skill improvements and observe changes in their career match scores.
- **AI-Powered Career Roadmap:** Generates a personalized five-step career development pathway using Google Gemini AI.
- **Fallback Mechanism:** Provides alternative guidance when the generative AI service is unavailable.

## Technologies Used

- Python
- Streamlit
- Pandas
- PyMuPDF
- Pydantic
- Google Gemini API
- O*NET 31.0 Occupational Database
- CSV-based Career Knowledge Base

## System Workflow

1. Upload a resume or manually enter student information.
2. Extract and verify relevant skills and profile information.
3. Assess individual skill proficiency levels.
4. Match student skills with occupational requirements.
5. Generate personalized career recommendations.
6. Identify skill gaps and development targets.
7. Simulate potential skill improvements.
8. Generate a personalized five-step career roadmap.

## Career Knowledge Base

The system uses a structured career knowledge base derived from O*NET 31.0, covering 19 career roles related to Computer Science and Information Technology.

The knowledge base includes occupational descriptions, essential skills, knowledge areas, software skills, and O*NET occupation codes.

## Objectives

- Support personalized career exploration among university students.
- Identify gaps between existing student skills and occupational requirements.
- Provide practical recommendations for skill development.
- Enable interactive exploration of potential career pathways.
- Support informed academic and career-related decisions.

## Sustainable Development Goals

- **SDG 4 – Quality Education:** Supports personalized learning and skill development.
- **SDG 8 – Decent Work and Economic Growth:** Supports career readiness and informed employment decisions.

## Future Scope

- Expansion of the career knowledge base.
- Integration of real-time labour market trends.
- Incorporation of alumni career trajectories.
- Improved resume analysis and skill normalization.
- Integration of verified learning resources and certification platforms.
- Evaluation through student and career counsellor feedback.

## Status

✅ Functional Prototype Developed

The core features of the application have been implemented. Further improvements and evaluation can be carried out to enhance recommendation quality and expand career coverage.

## Disclaimer
The application is intended to support career exploration and decision-making. Career match scores indicate alignment with the skills represented in the knowledge base and do not guarantee employment or career success.

