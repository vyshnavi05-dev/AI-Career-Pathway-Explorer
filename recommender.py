
from google import genai
from pydantic import BaseModel, Field
from typing import List

from career_matcher import calculate_career_matches


client = genai.Client()


class SkillTarget(BaseModel):
    skill: str
    target_level: int = Field(ge=1, le=5)
    reason: str


class CareerRecommendation(BaseModel):
    career: str
    match_percentage: float
    why_it_fits: str
    matched_skills: List[str]
    missing_skills: List[str]
    skill_targets: List[SkillTarget]
    learning_suggestions: List[str]
    project_suggestions: List[str]
    certification_suggestions: List[str]
    higher_studies: List[str]


class CareerAnalysis(BaseModel):
    recommendations: List[CareerRecommendation]


def recommend_careers(
    proficiency,
    education="",
    interests="",
    projects="",
    certifications="",
    preferences=""
):

    # --------------------------------------------------
    # STEP 1: Calculate career matches using O*NET
    # --------------------------------------------------

    career_matches = calculate_career_matches(proficiency)

    if not career_matches:
        return None

    # Keep the strongest candidates for Gemini.
    top_matches = career_matches[:5]


    # --------------------------------------------------
    # STEP 2: Prepare career knowledge for Gemini
    # --------------------------------------------------

    career_information = []

    for career in top_matches:

        career_information.append(
            {
                "career": career["career"],
                "onet_code": career["onet_code"],
                "description": career["description"],
                "match_percentage": career["match_percentage"],
                "matched_skills": career["matched_skills"],
                "missing_skills": career["missing_skills"],
                "career_skills": career["career_skills"],
            }
        )


    # --------------------------------------------------
    # STEP 3: Prepare student profile
    # --------------------------------------------------

    skill_information = []

    for skill, level in proficiency.items():

        skill_information.append(
            f"{skill}: {level}/5"
        )


    student_profile = f"""
Education:
{education}

Interests:
{interests}

Projects:
{projects}

Certifications:
{certifications}

Career preferences:
{preferences}

Current skill proficiency:
{", ".join(skill_information)}
"""


    # --------------------------------------------------
    # Certification options
    # --------------------------------------------------

    certification_options = [
        "CompTIA A+",
        "CompTIA Network+",
        "CompTIA Security+",
        "CompTIA Linux+",
        "AWS Certified Cloud Practitioner",
        "AWS Certified Developer - Associate",
        "AWS Certified Solutions Architect - Associate",
        "Microsoft Certified: Azure Fundamentals",
        "Microsoft Certified: Azure Administrator Associate",
        "Cisco Certified Support Technician (CCST) Networking",
        "Cisco Certified Support Technician (CCST) Cybersecurity",
        "Certified Information Systems Auditor (CISA)",
        "Certified Information Security Manager (CISM)",
        "Google Cybersecurity Certificate",
        "Linux Professional Institute Certification (LPIC-1)",
    ]


    # --------------------------------------------------
    # STEP 4: Ask Gemini to personalize the results
    # --------------------------------------------------

    prompt = f"""
You are the personalization layer of an AI Career Pathway
Explorer.

A Python-based career matching system has already compared the
student's skills against an O*NET 31.0-derived career knowledge
base.

Your job is NOT to independently invent career recommendations.

Instead:

1. Select exactly 3 careers from the provided career candidates.
2. Explain why each selected career fits the student's profile.
3. Use the supplied matched and missing skills.
4. Suggest practical skills the student should learn.
5. Suggest realistic projects for building those skills.
6. Suggest relevant certification areas.
7. Suggest suitable higher-study directions.
8. Suggest relevant certifications ONLY from the provided certification list.
9. Identify the most useful skills for the student to improve for
   each specific career.
10. Give a realistic target proficiency level from 1 to 5 for each
    selected improvement skill.

IMPORTANT RULES:

- Only recommend careers from the provided candidate list.
- Do not invent careers.
- Do not change the supplied match percentages.
- Do not claim that the match percentage is an official O*NET score.
- The percentage is calculated by our application's matching
  algorithm using O*NET-derived requirements.
- Do not invent information about the student's education,
  projects, certifications, interests, or preferences.
- Personalize the explanation using the student's profile.
- Keep suggestions practical for a university student.
- Higher-study suggestions should be general academic directions,
  not claims about admission eligibility.

MATCH PERCENTAGE RULES:

- For each recommendation, return the match_percentage exactly as
  provided in the candidate career information.
- Do not calculate, modify, round, increase, or decrease the
  supplied match percentage.
- The match percentage is calculated by the application's Python
  skill-matching algorithm using O*NET-derived career requirements.
- It is not an official O*NET score.

SKILL TARGET RULES:

For each recommended career, return 3 to 5 skill targets.

Each skill target must contain:

- skill: the exact skill name from that career's career_skills,
  matched_skills, or missing_skills.
- target_level: the proficiency level from 1 to 5 that the student
  should aim for.
- reason: a short explanation of why improving this skill matters
  for this specific career.

IMPORTANT:

- Use the exact canonical skill names provided by the career data.
- Do not invent new skill names.
- Do not combine multiple skills into one skill name.
  For example, use "Splunk" and "SIEM" separately if both are
  relevant.
- Prefer skills that are important for the specific career.
- Include both important existing skills that could be strengthened
  and important missing skills when appropriate.
- If the student already has a skill at level 4 or 5, do not
  recommend increasing it unless there is a clear reason.
- A target level should normally be higher than the student's
  current level when improvement is recommended.
- Do not recommend a target level above 5.
- Do not recommend unnecessary improvements to unrelated skills.
- The target level should be realistic for a university student,
  not an assumption of expert-level mastery.
- The skill targets should be specific to each career. Do not return
  the same generic skill list for every career unless the career
  requirements genuinely overlap.

The skill targets will be used by the application's What-If
simulator to show:

Current level → Target level

and calculate a projected career match when the user increases
their proficiency.

STUDENT PROFILE
----------------
{student_profile}
----------------

O*NET-DERIVED CAREER CANDIDATES
--------------------------------
{career_information}
--------------------------------

AVAILABLE CERTIFICATIONS
------------------------
{certification_options}
----------------

Certification rules:

- Only use certifications from the available certification list.
- Do not invent or rename certification titles.
- If no certification is particularly relevant, provide an empty list.

Return exactly 3 recommendations.
"""


    # --------------------------------------------------
    # STEP 5: Structured Gemini response
    # --------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": CareerAnalysis,
            },
        )

        analysis = CareerAnalysis.model_validate_json(
            response.text
        )


        # --------------------------------------------------
        # STEP 6: Validate Gemini skill targets
        # --------------------------------------------------

        for recommendation in analysis.recommendations:

            # Find the original career information.
            original_career = None

            for career in top_matches:
                if career["career"] == recommendation.career:
                    original_career = career
                    break

            if original_career is None:
                continue

            allowed_skills = set(
                original_career["career_skills"]
            )

            valid_targets = []

            for target in recommendation.skill_targets:

                # Only allow skills that actually belong to
                # this career's O*NET-derived skill set.
                if target.skill not in allowed_skills:
                    continue

                current_level = proficiency.get(
                    target.skill,
                    0
                )

                # Keep the target within 1-5.
                target_level = max(
                    1,
                    min(target.target_level, 5)
                )

                # Never make an improvement target lower than
                # the student's current level.
                if current_level > 0:
                    target_level = max(
                        current_level,
                        target_level
                    )

                target.target_level = target_level

                valid_targets.append(target)

            recommendation.skill_targets = valid_targets


            # --------------------------------------------------
            # Fallback if Gemini returns no valid targets
            # --------------------------------------------------

            if not recommendation.skill_targets:

                fallback_targets = []

                for skill in original_career["career_skills"]:

                    current_level = proficiency.get(
                        skill,
                        0
                    )

                    if current_level < 5:

                        fallback_targets.append(
                            SkillTarget(
                                skill=skill,
                                target_level=min(
                                    current_level + 2,
                                    5
                                ),
                                reason=(
                                    "Improving this skill can "
                                    "strengthen alignment with "
                                    "the career's requirements."
                                )
                            )
                        )

                    if len(fallback_targets) >= 5:
                        break

                recommendation.skill_targets = fallback_targets


        return analysis


    except Exception as e:

        print(
            "❌ Gemini recommender error:",
            repr(e)
        )

        return None
