
import streamlit as st
import fitz

from skill_extractor import extract_skills
from recommender import recommend_careers
from ai_pathway import generate_pathway
from resume_parser import extract_resume_profile
from career_matcher import calculate_projected_match


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Career Pathway Explorer",
    page_icon=None,
    layout="wide"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* ==================================================
       COLOUR PALETTE
       ================================================== */

    :root {
        --cream: #ECDFCC;
        --light-panel: #F7F1E7;
        --olive: #697565;
        --dark-gray: #3C3D37;
        --dark: #1E201E;
    }


    /* ==================================================
       PAGE
       ================================================== */

    .stApp {
        background-color: #ECDFCC;
    }

    .main {
        background-color: #ECDFCC;
    }

    html, body {
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    }


    /* ==================================================
       NORMAL TEXT
       ================================================== */

    .stApp p {
        color: #1E201E;
    }

    .stApp label {
        color: #1E201E;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {
        color: #1E201E;
    }


    /* ==================================================
       MAIN TITLE
       ================================================== */

    .main-title {
        background-color: #1E201E;
        color: #ECDFCC !important;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        padding: 28px 32px 6px 32px;
        border-radius: 14px 14px 0 0;
        margin: 0 !important;
        border: 1px solid #697565;
        border-bottom: none;
    }

    .main-subtitle {
        background-color: #1E201E;
        color: #ECDFCC !important;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif !important;
        font-size: 1.05rem !important;
        padding: 6px 32px 28px 32px;
        border-radius: 0 0 14px 14px;
        margin: 0 0 30px 0 !important;
        border: 1px solid #697565;
        border-top: none;
    }


    /* ==================================================
       TEXT INPUTS
       ================================================== */

    div[data-baseweb="input"] {
        background-color: #F7F1E7 !important;
        border: 1.5px solid #697565 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="input"] > div {
        background-color: #F7F1E7 !important;
    }

    input {
        color: #1E201E !important;
        background-color: #F7F1E7 !important;
        caret-color: #1E201E !important;
    }

    input::placeholder {
        color: #697565 !important;
        opacity: 1 !important;
    }


    /* ==================================================
       TEXT AREAS
       ================================================== */

    div[data-baseweb="textarea"] {
        background-color: #F7F1E7 !important;
        border: 1.5px solid #697565 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="textarea"] > div {
        background-color: #F7F1E7 !important;
    }

    textarea {
        color: #1E201E !important;
        background-color: #F7F1E7 !important;
        caret-color: #1E201E !important;
    }

    textarea::placeholder {
        color: #697565 !important;
        opacity: 1 !important;
    }


    /* ==================================================
       INPUT FOCUS
       ================================================== */

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within {
        border-color: #3C3D37 !important;
        box-shadow: 0 0 0 1px #3C3D37 !important;
    }


    /* ==================================================
       FILE UPLOADER
       ================================================== */

    section[data-testid="stFileUploaderDropzone"] {
        background-color: #F7F1E7 !important;
        border: 2px dashed #697565 !important;
        border-radius: 12px !important;
    }

    section[data-testid="stFileUploaderDropzone"] > div {
        background-color: #F7F1E7 !important;
    }

    section[data-testid="stFileUploaderDropzone"] p {
        color: #1E201E !important;
    }

    section[data-testid="stFileUploaderDropzone"] small {
        color: #3C3D37 !important;
    }

    section[data-testid="stFileUploaderDropzone"] button {
        background-color: #697565 !important;
        color: #ECDFCC !important;
        border: 1px solid #3C3D37 !important;
        border-radius: 7px !important;
    }

    section[data-testid="stFileUploaderDropzone"] button * {
        color: #ECDFCC !important;
    }


    /* Uploaded file */

    [data-testid="stFileUploaderFile"] {
        background-color: #F7F1E7 !important;
        border: 1px solid #697565 !important;
        border-radius: 8px !important;
    }

    [data-testid="stFileUploaderFile"] p,
    [data-testid="stFileUploaderFile"] span,
    [data-testid="stFileUploaderFile"] small {
        color: #1E201E !important;
    }

    [data-testid="stFileUploaderFileName"] {
        color: #1E201E !important;
    }


    /* ==================================================
       BUTTONS
       ================================================== */

    .stButton > button {
        background-color: #697565 !important;
        color: #ECDFCC !important;
        border: 1.5px solid #3C3D37 !important;
        border-radius: 9px !important;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif !important;
        font-weight: 600 !important;
        min-height: 42px !important;
    }

    .stButton > button p,
    .stButton > button span {
        color: #ECDFCC !important;
    }

    .stButton > button:hover {
        background-color: #3C3D37 !important;
        border-color: #1E201E !important;
    }


    /* ==================================================
       RADIO BUTTONS
       ================================================== */

    div[role="radiogroup"] {
        background-color: transparent !important;
    }

    div[role="radiogroup"] label {
        color: #1E201E !important;
    }

    div[role="radiogroup"] label p {
        color: #1E201E !important;
    }


    /* ==================================================
       DROPDOWNS
       ================================================== */

    div[data-baseweb="select"] > div {
        background-color: #F7F1E7 !important;
        border: 1.5px solid #697565 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] span {
        color: #1E201E !important;
    }

    div[data-baseweb="select"] input {
        color: #1E201E !important;
    }


    /* ==================================================
       CUSTOM DROPDOWN ARROW
       ================================================== */

    div[data-baseweb="select"] > div > div:last-child {
        position: relative !important;
        width: 32px !important;
        color: transparent !important;
    }

    div[data-baseweb="select"] > div > div:last-child svg {
        display: none !important;
    }

    div[data-baseweb="select"] > div > div:last-child::after {
        content: "";
        position: absolute;
        top: 50%;
        right: 12px;
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #1E201E;
        transform: translateY(-35%);
    }


    /* Dropdown menu */

    div[data-baseweb="popover"] {
        background-color: #F7F1E7 !important;
        border: 1px solid #697565 !important;
    }

    div[data-baseweb="popover"] ul {
        background-color: #F7F1E7 !important;
    }

    div[data-baseweb="popover"] li {
        background-color: #F7F1E7 !important;
        color: #1E201E !important;
    }

    div[data-baseweb="popover"] li:hover {
        background-color: #ECDFCC !important;
        color: #1E201E !important;
    }


    /* ==================================================
       EXPANDERS
       ================================================== */

    div[data-testid="stExpander"] {
        background-color: #F7F1E7 !important;
        border: 1px solid #697565 !important;
        border-radius: 10px !important;
    }

    div[data-testid="stExpander"] summary {
        background-color: #F7F1E7 !important;
    }

    div[data-testid="stExpander"] summary p {
        color: #1E201E !important;
        font-weight: 600 !important;
    }

    div[data-testid="stExpander"] summary:hover {
        background-color: #ECDFCC !important;
    }


    /* ==================================================
       PATHWAY CONTENT
       ================================================== */

    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] li,
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] strong,
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] em {
        color: #1E201E !important;
    }

    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        color: #1E201E !important;
    }

    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] ul,
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] ol {
        color: #1E201E !important;
    }


    /* ==================================================
       SLIDERS
       ================================================== */

    div[data-testid="stSlider"] label {
        color: #1E201E !important;
    }

    div[data-testid="stSlider"] label p {
        color: #1E201E !important;
    }

    div[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
        color: #3C3D37 !important;
    }

    div[data-baseweb="slider"] > div > div > div {
        background-color: #697565 !important;
    }

    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #3C3D37 !important;
        border-color: #3C3D37 !important;
    }


    /* ==================================================
       INFO / SUCCESS / WARNING
       ================================================== */

    div[data-testid="stAlert"] {
        background-color: #F7F1E7 !important;
        border: 1px solid #697565 !important;
    }

    div[data-testid="stAlert"] p {
        color: #1E201E !important;
    }


    /* ==================================================
       CAPTIONS
       ================================================== */

    [data-testid="stCaptionContainer"] p {
        color: #3C3D37 !important;
    }


    /* ==================================================
       DIVIDERS
       ================================================== */

    hr {
        border-color: #697565 !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# PROFICIENCY FUNCTION
# --------------------------------------------------

def get_proficiency(skills):

    proficiency = {}

    st.subheader("Rate Your Skill Proficiency")

    st.info(
        "Rate your practical ability in each skill. "
        "Studying a skill does not necessarily mean you can use it confidently."
    )

    for skill in skills:

        level = st.slider(
            skill,
            min_value=1,
            max_value=5,
            value=2,
            key=f"proficiency_{skill}"
        )

        if level == 1:
            description = "Familiar"
        elif level == 2:
            description = "Beginner"
        elif level == 3:
            description = "Intermediate"
        elif level == 4:
            description = "Advanced"
        else:
            description = "Highly proficient"

        st.caption(
            f"{level}/5 · {description}"
        )

        proficiency[skill] = level

    return proficiency


# --------------------------------------------------
# PATHWAY DISPLAY
# --------------------------------------------------

def display_pathway(pathway):

    if not pathway:

        st.warning(
            "A personalized pathway could not be generated."
        )

        return

    # --------------------------------------------------
    # Clean malformed skill-target Markdown
    # --------------------------------------------------

    import re

    # Fix cases such as:
    # \**- **Wireshark (2/5 → 4/5)** - explanation
    #
    # into:
    # - **Wireshark (2/5 → 4/5)** - explanation

    pathway = re.sub(
        r'\\\*\*-\s*\*\*([^*]+?)\*\*',
        r'- **\1**',
        pathway
    )

    # Fix cases where Gemini produces:
    # - **Skill (2/5 → 4/5)** - explanation
    #
    # and cases where the opening bold marker is malformed.

    pathway = re.sub(
        r'\\\*\*-\s*\*\*',
        '- **',
        pathway
    )

    # --------------------------------------------------
    # Parse pathway steps
    # --------------------------------------------------

    lines = pathway.splitlines()

    current_step = None
    current_content = []

    steps = []

    for line in lines:

        stripped = line.strip()

        if stripped.lower().startswith("### step"):

            if current_step is not None:

                steps.append(
                    (
                        current_step,
                        "\n".join(current_content)
                    )
                )

            current_step = stripped.replace(
                "###",
                ""
            ).strip()

            current_content = []

        else:

            if current_step is not None:

                current_content.append(line)

    if current_step is not None:

        steps.append(
            (
                current_step,
                "\n".join(current_content)
            )
        )

    # --------------------------------------------------
    # Display pathway
    # --------------------------------------------------

    if steps:

        for title, content in steps:

            with st.expander(title):

                st.markdown(content)

    else:

        st.markdown(pathway)

# --------------------------------------------------
# WHAT-IF SIMULATOR
# --------------------------------------------------

def show_what_if_simulator(
    recommendation,
    proficiency
):

    st.markdown(
        "### What If You Improve Your Skills?"
    )

    st.caption(
        "Experiment with the career-specific skill targets "
        "to see how improving your proficiency could affect "
        "your application match."
    )

    simulated_proficiency = proficiency.copy()


    # --------------------------------------------------
    # Use structured targets from Gemini
    # --------------------------------------------------

    skill_targets = recommendation.skill_targets


    if not skill_targets:

        st.info(
            "No specific skill improvement targets were identified "
            "for this career."
        )

        return


    for target in skill_targets:

        skill = target.skill

        current_level = proficiency.get(
            skill,
            0
        )

        target_level = max(
            current_level,
            min(target.target_level, 5)
        )


        # Show current and target level clearly.
        st.markdown(
            f"**{skill}**  "
            f"Current: {current_level}/5 → "
            f"Target: {target_level}/5"
        )


        # Slider starts at the student's current level.
        simulated_level = st.slider(
            f"Improve {skill}",
            min_value=current_level,
            max_value=5,
            value=current_level,
            key=f"what_if_{recommendation.career}_{skill}"
        )


        simulated_proficiency[skill] = simulated_level


        if target.reason:

            st.caption(
                target.reason
            )


    # --------------------------------------------------
    # Calculate projected match
    # --------------------------------------------------

    projected_match = calculate_projected_match(
        simulated_proficiency,
        recommendation.career
    )


    if projected_match:

        current_match = recommendation.match_percentage

        projected_percentage = projected_match[
            "match_percentage"
        ]


        st.markdown(
            f"**Current Match:** {current_match:.1f}%"
        )

        st.markdown(
            f"**Projected Match:** {projected_percentage:.1f}%"
        )


        difference = (
            projected_percentage
            - current_match
        )


        if difference > 0:

            st.success(
                f"Projected improvement: "
                f"+{difference:.1f} percentage points"
            )

        elif difference == 0:

            st.info(
                "No change in the projected match yet. "
                "Try increasing one or more skills."
            )

        else:

            st.info(
                f"Projected change: "
                f"{difference:.1f} percentage points"
            )


# --------------------------------------------------
# CAREER RECOMMENDATION FUNCTION
# --------------------------------------------------

def show_recommendations(
    proficiency,
    education="",
    interests="",
    projects="",
    certifications="",
    preferences=""
):

    # Generate the Gemini career analysis only once.
    if "career_analysis" not in st.session_state:

        with st.spinner(
            "Analyzing your profile..."
        ):

            analysis = recommend_careers(
                proficiency,
                education=education,
                interests=interests,
                projects=projects,
                certifications=certifications,
                preferences=preferences
            )

        st.session_state[
            "career_analysis"
        ] = analysis

    else:

        analysis = st.session_state[
            "career_analysis"
        ]


    if analysis is None:

        st.error(
            "The recommendation service could not complete "
            "the analysis. Please try again."
        )

        return


    st.subheader(
        "Recommended Career Paths"
    )

    st.caption(
        "Career recommendations are generated using the "
        "application's skill-matching system and an "
        "O*NET-derived career knowledge base."
    )


    for recommendation in analysis.recommendations:

        with st.expander(
            recommendation.career,
            expanded=True
        ):

            st.markdown(
                f"**Application Match: "
                f"{recommendation.match_percentage:.1f}%**"
            )

            st.caption(
                "Calculated by the application's skill-matching "
                "algorithm using O*NET-derived career requirements."
            )


            # --------------------------------------------------
            # WHAT-IF SIMULATOR
            # --------------------------------------------------

            with st.expander(
                "What If You Improve Your Skills?"
            ):

                show_what_if_simulator(
                    recommendation,
                    proficiency
                )


            # --------------------------------------------------
            # WHY THIS FITS
            # --------------------------------------------------

            with st.expander(
                "Why This Fits You",
                expanded=True
            ):

                st.write(
                    recommendation.why_it_fits
                )


            # --------------------------------------------------
            # RELEVANT SKILLS
            # --------------------------------------------------

            with st.expander(
                "Your Relevant Skills"
            ):

                if recommendation.matched_skills:

                    for skill in recommendation.matched_skills:

                        st.write(
                            "•",
                            skill
                        )

                else:

                    st.write(
                        "No directly matched skills identified."
                    )


            # --------------------------------------------------
            # SKILLS TO DEVELOP
            # --------------------------------------------------

            with st.expander(
                "Skills to Develop"
            ):

                if recommendation.missing_skills:

                    for skill in recommendation.missing_skills:

                        st.write(
                            "•",
                            skill
                        )

                else:

                    st.write(
                        "No major skill gaps identified."
                    )


            # --------------------------------------------------
            # LEARNING SUGGESTIONS
            # --------------------------------------------------

            with st.expander(
                "How to Develop These Skills"
            ):

                for suggestion in (
                    recommendation.learning_suggestions
                ):

                    st.write(
                        "•",
                        suggestion
                    )


            # --------------------------------------------------
            # PROJECT SUGGESTIONS
            # --------------------------------------------------

            with st.expander(
                "Suggested Projects"
            ):

                for project in (
                    recommendation.project_suggestions
                ):

                    st.write(
                        "•",
                        project
                    )


            # --------------------------------------------------
            # CERTIFICATION SUGGESTIONS
            # --------------------------------------------------

            with st.expander(
                "Suggested Certifications"
            ):

                for certification in (
                    recommendation.certification_suggestions
                ):

                    st.write(
                        "•",
                        certification
                    )


            # --------------------------------------------------
            # HIGHER STUDIES
            # --------------------------------------------------

            with st.expander(
                "Higher-Study Directions"
            ):

                for study in (
                    recommendation.higher_studies
                ):

                    st.write(
                        "•",
                        study
                    )


            # --------------------------------------------------
            # PERSONALIZED PATHWAY
            # --------------------------------------------------

            with st.expander(
                "Personalized Career Pathway"
            ):

                pathway_key = (
                    f"pathway_{recommendation.career}"
                )


                if pathway_key not in st.session_state:

                    with st.spinner(
                        "Creating your personalized pathway..."
                    ):

                        pathway = generate_pathway(
                            recommendation.career,
                            recommendation.matched_skills,
                            recommendation.missing_skills,
                            skill_targets=recommendation.skill_targets,
                            education=education,
                            interests=interests,
                            projects=projects,
                            certifications=certifications,
                            preferences=preferences
                        )

                    st.session_state[
                        pathway_key
                    ] = pathway

                else:

                    pathway = st.session_state[
                        pathway_key
                    ]


                display_pathway(
                    pathway
                )


        st.divider()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">'
    'AI Career Pathway Explorer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Explore career pathways based on your skills, experience, '
    'interests, and proficiency.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# INPUT METHOD
# --------------------------------------------------

st.subheader(
    "Enter Your Profile"
)

input_method = st.radio(
    "Choose an input method",
    [
        "Upload Resume",
        "Enter Information Manually"
    ],
    horizontal=True
)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

if input_method == "Upload Resume":

    resume = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )


    if resume is not None:

        st.success(
            "Resume uploaded successfully."
        )


        pdf = fitz.open(
            stream=resume.read(),
            filetype="pdf"
        )


        resume_text = ""


        for page in pdf:

            resume_text += page.get_text()


        skills = extract_skills(
            resume_text
        )


        with st.spinner(
            "Reading your resume..."
        ):

            resume_profile = extract_resume_profile(
                resume_text
            )


        if resume_profile is None:

            st.error(
                "The system could not extract your profile "
                "information. Please try uploading the "
                "resume again."
            )


        elif skills:

            with st.expander(
                "Skills Found in Your Resume",
                expanded=True
            ):

                for skill in skills:

                    st.write(
                        "•",
                        skill
                    )


            proficiency = get_proficiency(
                skills
            )


            st.subheader(
                "Review Your Profile"
            )


            st.info(
                "Information detected from your resume has been "
                "pre-filled. You can edit anything that needs correction."
            )


            education = st.text_area(
                "Education / Qualifications",
                value=resume_profile.education,
                placeholder="Example: B.Tech Computer Science"
            )


            projects = st.text_area(
                "Projects",
                value="\n".join(
                    resume_profile.projects
                ),
                placeholder=(
                    "Example: Network Intrusion Detection System"
                )
            )


            certifications = st.text_area(
                "Certifications",
                value="\n".join(
                    resume_profile.certifications
                ),
                placeholder=(
                    "Example: Google Cybersecurity Certificate"
                )
            )


            interests = st.text_area(
                "Interests",
                value=", ".join(
                    resume_profile.interests
                ),
                placeholder=(
                    "Example: Cybersecurity, Digital Forensics, "
                    "Ethical Hacking"
                )
            )


            preferences = st.text_area(
                "Career Preferences",
                value=resume_profile.career_preferences,
                placeholder=(
                    "Example: Prefer practical technical work, "
                    "interested in cybersecurity, "
                    "prefer programming over data science"
                )
            )


            profile_confirmed = st.button(
                "Confirm Profile and Explore Careers"
            )


            if profile_confirmed:

                # Save the confirmed profile so that Streamlit
                # reruns do not destroy the analysis screen.

                st.session_state[
                    "profile_confirmed"
                ] = True


                st.session_state[
                    "confirmed_proficiency"
                ] = proficiency


                st.session_state[
                    "confirmed_education"
                ] = education


                st.session_state[
                    "confirmed_interests"
                ] = interests


                st.session_state[
                    "confirmed_projects"
                ] = projects


                st.session_state[
                    "confirmed_certifications"
                ] = certifications


                st.session_state[
                    "confirmed_preferences"
                ] = preferences


                # Clear any previous analysis/pathways
                # because the user has just confirmed
                # a new profile.

                st.session_state.pop(
                    "career_analysis",
                    None
                )


                for key in list(
                    st.session_state.keys()
                ):

                    if key.startswith(
                        "pathway_"
                    ):

                        del st.session_state[key]


            if st.session_state.get(
                "profile_confirmed",
                False
            ):

                show_recommendations(
                    st.session_state[
                        "confirmed_proficiency"
                    ],
                    education=st.session_state.get(
                        "confirmed_education",
                        ""
                    ),
                    interests=st.session_state.get(
                        "confirmed_interests",
                        ""
                    ),
                    projects=st.session_state.get(
                        "confirmed_projects",
                        ""
                    ),
                    certifications=st.session_state.get(
                        "confirmed_certifications",
                        ""
                    ),
                    preferences=st.session_state.get(
                        "confirmed_preferences",
                        ""
                    )
                )


        else:

            st.warning(
                "No skills were detected from the resume."
            )


            st.info(
                "Please try entering your information manually "
                "using the manual input option."
            )


# --------------------------------------------------
# MANUAL INPUT
# --------------------------------------------------

else:

    st.subheader(
        "Enter Your Information"
    )


    education = st.text_input(
        "Education",
        placeholder="Example: B.Tech Computer Science"
    )


    manual_skills = st.text_area(
        "Skills",
        placeholder="Example: Python, Linux, SQL, Networking"
    )


    interests = st.text_area(
        "Interests",
        placeholder=(
            "Example: Cybersecurity, Digital Forensics, "
            "Ethical Hacking"
        )
    )


    projects = st.text_area(
        "Projects",
        placeholder=(
            "Example: Network Intrusion Detection System"
        )
    )


    certifications = st.text_area(
        "Certifications",
        placeholder=(
            "Example: Google Cybersecurity Certificate"
        )
    )


    preferences = st.text_area(
        "Career Preferences",
        placeholder=(
            "Example: Prefer practical technical work, "
            "interested in cybersecurity, "
            "prefer programming over data science"
        )
    )


    if st.button(
        "Continue"
    ):

        skills = [
            skill.strip()
            for skill in manual_skills.split(",")
            if skill.strip()
        ]


        st.session_state[
            "manual_skills"
        ] = skills


        st.session_state[
            "education"
        ] = education


        st.session_state[
            "interests"
        ] = interests


        st.session_state[
            "projects"
        ] = projects


        st.session_state[
            "certifications"
        ] = certifications


        st.session_state[
            "preferences"
        ] = preferences


        # Clear previous analysis because the profile
        # has been changed.

        st.session_state.pop(
            "profile_confirmed",
            None
        )


        st.session_state.pop(
            "career_analysis",
            None
        )


        for key in list(
            st.session_state.keys()
        ):

            if key.startswith(
                "pathway_"
            ):

                del st.session_state[key]


        st.success(
            "Profile information received."
        )


    if "manual_skills" in st.session_state:

        skills = st.session_state[
            "manual_skills"
        ]


        with st.expander(
            "Skills You Entered",
            expanded=True
        ):

            for skill in skills:

                st.write(
                    "•",
                    skill
                )


        proficiency = get_proficiency(
            skills
        )


        if st.button(
            "Confirm Profile and Explore Careers"
        ):

            st.session_state[
                "profile_confirmed"
            ] = True


            st.session_state[
                "confirmed_proficiency"
            ] = proficiency


            st.session_state[
                "confirmed_education"
            ] = st.session_state.get(
                "education",
                ""
            )


            st.session_state[
                "confirmed_interests"
            ] = st.session_state.get(
                "interests",
                ""
            )


            st.session_state[
                "confirmed_projects"
            ] = st.session_state.get(
                "projects",
                ""
            )


            st.session_state[
                "confirmed_certifications"
            ] = st.session_state.get(
                "certifications",
                ""
            )


            st.session_state[
                "confirmed_preferences"
            ] = st.session_state.get(
                "preferences",
                ""
            )


            # Clear previous analysis/pathways
            # because the user has confirmed
            # a new profile.

            st.session_state.pop(
                "career_analysis",
                None
            )


            for key in list(
                st.session_state.keys()
            ):

                if key.startswith(
                    "pathway_"
                ):

                    del st.session_state[key]


        if st.session_state.get(
            "profile_confirmed",
            False
        ):

            show_recommendations(
                st.session_state[
                    "confirmed_proficiency"
                ],
                education=st.session_state.get(
                    "confirmed_education",
                    ""
                ),
                interests=st.session_state.get(
                    "confirmed_interests",
                    ""
                ),
                projects=st.session_state.get(
                    "confirmed_projects",
                    ""
                ),
                certifications=st.session_state.get(
                    "confirmed_certifications",
                    ""
                ),
                preferences=st.session_state.get(
                    "confirmed_preferences",
                    ""
                )
            )

