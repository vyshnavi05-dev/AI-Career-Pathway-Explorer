
from google import genai

client = genai.Client()


def generate_pathway(
    career,
    matched_skills,
    missing_skills,
    skill_targets=None,
    education="",
    interests="",
    projects="",
    certifications="",
    preferences=""
):

    # --------------------------------------------------
    # Prepare structured skill targets
    # --------------------------------------------------

    target_information = []

    if skill_targets:

        for target in skill_targets:

            # Works with the Pydantic SkillTarget object
            if hasattr(target, "skill"):

                skill = target.skill
                target_level = target.target_level
                reason = target.reason

            # Also supports dictionary data if needed
            else:

                skill = target.get("skill", "")
                target_level = target.get("target_level", 0)
                reason = target.get("reason", "")

            target_information.append(
                f"{skill}: target {target_level}/5 - {reason}"
            )

    if not target_information:
        target_information_text = "No structured skill targets provided."

    else:
        target_information_text = "\n".join(
            f"- {item}"
            for item in target_information
        )


    # --------------------------------------------------
    # Create pathway prompt
    # --------------------------------------------------

    prompt = f"""
You are an AI university career guidance assistant.

Create a practical, personalized career pathway for a university student.

Target career:
{career}

Student's existing relevant skills:
{", ".join(matched_skills) if matched_skills else "None identified"}

Skills to develop:
{", ".join(missing_skills) if missing_skills else "None identified"}


RECOMMENDED SKILL TARGETS
-------------------------
The career recommendation system has already identified the most
useful skills for this specific career and assigned target proficiency
levels.

Use these exact skill targets when discussing skill improvement:

{target_information_text}

IMPORTANT:
- Do not invent different target proficiency levels.
- Do not change the target levels provided above.
- When mentioning a skill target, show it as:
  Current Level → Target Level
- Determine the current level from the student's current skill
  information below.
- If the current level is 0 because the student has not demonstrated
  the skill, show 0/5 as the current level.
- Do not claim that the student already has a skill if it is not
  listed in their existing skills.
- Do not recommend improving a skill beyond the provided target
  unless there is a clear practical reason.
- The target level is a realistic development goal, not a claim that
  the student must become an expert.


STUDENT PROFILE
---------------

Education:
{education}

Interests:
{interests}

Existing Projects:
{projects}

Existing Certifications:
{certifications}

Career Preferences:
{preferences}


CURRENT SKILL PROFICIENCY
-------------------------

{", ".join(
    matched_skills
) if matched_skills else "No matched skills identified"}


PATHWAY REQUIREMENTS
--------------------

Create a clear pathway containing exactly 5 steps.

The pathway should include:

1. Strengthening the student's existing relevant skills.
2. Learning the most important missing skills.
3. Hands-on practice and suitable projects.
4. Building a portfolio and gaining relevant experience.
5. Preparing for internships, entry-level roles, or higher studies.


STEP 1 REQUIREMENTS
-------------------

Step 1 is especially important.

Use the provided RECOMMENDED SKILL TARGETS to explain which
existing skills should be strengthened and which relevant skills
should be developed.

For each useful skill target, show the skill name AND the
current-to-target proficiency in BOLD Markdown.

The required format is EXACTLY:

- **Skill (current/5 → target/5)** - Explanation of what the student
  should do to reach the target.

For example:

- **Python (2/5 → 3/5)** - Practice writing automation scripts
  and apply Python to practical career-related tasks.

IMPORTANT FORMATTING RULE:

- ALWAYS wrap the entire "Skill (current/5 → target/5)" portion in
  double asterisks for Markdown bold.
- NEVER output the skill target without ** around it.
- Do not bold the explanation unless necessary.
- Use the student's actual current proficiency and the provided
  target proficiency.
- Do not change the provided target level.

Do not use an example skill unless it is actually present in the
provided skill targets.


PERSONALIZATION RULES
---------------------

- Personalize the pathway using the student's profile.
- Build upon existing projects, certifications, interests, and
  existing skills when relevant.
- Prioritize the provided skill targets.
- Use the student's actual current proficiency when describing
  improvement.
- Do not recommend learning skills the student already demonstrates
  at a strong level unless there is a clear reason.
- Do not invent projects, certifications, experience, interests,
  qualifications, or achievements.
- Suggested projects should be realistic for a university student.
- Connect projects to the target career and the skills being
  developed.
- Keep the pathway practical and achievable.
- Avoid generic motivational filler.
- Keep each step concise but useful.
- The pathway must contain exactly 5 steps.

MARKDOWN FORMATTING REQUIREMENTS
--------------------------------

The pathway is displayed directly in a Markdown-enabled interface.

Therefore:

- Use Markdown bold syntax exactly as instructed.
- Every skill target in Step 1 MUST have the skill and
  current-to-target levels in bold.
- Example:
  - **Networking (0/5 → 4/5)** - Explanation
  - **Linux (0/5 → 4/5)** - Explanation
  - **Python (2/5 → 3/5)** - Explanation
- Do not remove the double asterisks.
- Do not replace Markdown bold with plain text.

OUTPUT FORMAT
-------------

Use exactly this format:

### Step 1: [Title]

[Content]

### Step 2: [Title]

[Content]

### Step 3: [Title]

[Content]

### Step 4: [Title]

[Content]

### Step 5: [Title]

[Content]
"""


    # --------------------------------------------------
    # Generate pathway
    # --------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text


    except Exception as e:

        print(
            "❌ Pathway generation error:",
            repr(e)
        )

        return (
            "### Step 1: Strengthen Your Existing Skills\n\n"
            f"Strengthen the skills most relevant to {career} "
            "and apply them through practical exercises.\n\n"
            
            "### Step 2: Learn Key Missing Skills\n\n"
            "Focus on the most important skills identified for "
            "your target career.\n\n"
            
            "### Step 3: Build Hands-On Experience\n\n"
            "Practice the skills through small, practical projects "
            "related to the target career.\n\n"
            
            "### Step 4: Build Your Portfolio\n\n"
            "Document your projects and demonstrate the skills "
            "you have developed.\n\n"
            
            "### Step 5: Prepare for Opportunities\n\n"
            "Prepare your resume and portfolio for internships, "
            "entry-level opportunities, or higher studies."
        )

