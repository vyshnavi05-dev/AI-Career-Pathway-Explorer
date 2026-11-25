import pandas as pd


# Maps O*NET software / technology names to the standardized
# skills used by our application.
SKILL_ALIASES = {
    "python": "Python",
    "python programming language": "Python",

    "java": "Java",
    "java programming language": "Java",

    "c": "C",
    "c programming language": "C",

    "c++": "C++",
    "c++ programming language": "C++",

    "javascript": "JavaScript",
    "javascript programming language": "JavaScript",

    "sql": "SQL",
    "structured query language": "SQL",
    "microsoft sql server": "SQL",
    "mysql": "SQL",
    "postgresql": "SQL",
    "oracle database": "SQL",

    "html": "HTML",
    "hypertext markup language": "HTML",

    "css": "CSS",
    "cascading style sheets": "CSS",

    "linux": "Linux",
    "ubuntu": "Linux",
    "red hat enterprise linux": "Linux",
    "unix": "Linux",

    "windows": "Windows",
    "microsoft windows": "Windows",

    "git": "Git",
    "github": "Git",

    "docker": "Docker",

    "amazon web services": "AWS",
    "aws": "AWS",

    "microsoft azure": "Azure",
    "azure": "Azure",

    "wireshark": "Wireshark",
    "nmap": "Nmap",
    "splunk": "Splunk",

    "networking": "Networking",
    "computer networking": "Networking",

    "network security": "Network Security",

    "cybersecurity": "Cybersecurity",
    "cyber security": "Cybersecurity",
    "information security": "Cybersecurity",

    "security information and event management": "SIEM",
    "siem": "SIEM",

    "incident response": "Incident Response",
    "threat analysis": "Threat Analysis",
    "log analysis": "Log Analysis",

    "ethical hacking": "Ethical Hacking",
    "penetration testing": "Penetration Testing",

    "digital forensics": "Digital Forensics",
    "computer forensics": "Digital Forensics",

    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",

    "data analysis": "Data Analysis",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "tensorflow": "TensorFlow",
    "scikit-learn": "Scikit-learn",
    "statistics": "Statistics",
}


def load_career_knowledge_base():
    return pd.read_csv("career_knowledge_base.csv")


def normalize_skill(text):
    text = str(text).strip().lower()

    if text in SKILL_ALIASES:
        return SKILL_ALIASES[text]

    for alias, normalized_skill in SKILL_ALIASES.items():
        if alias in text:
            return normalized_skill

    return None


def extract_career_skills(row):

    career_skills = set()

    # --------------------------------------------------
    # 1. O*NET SOFTWARE SKILLS
    # --------------------------------------------------

    software_text = str(row.get("software_skills", ""))

    if software_text and software_text != "nan":

        for item in software_text.split(";"):

            normalized = normalize_skill(item)

            if normalized:
                career_skills.add(normalized)

    # --------------------------------------------------
    # 2. SELECTED O*NET KNOWLEDGE AREAS
    # --------------------------------------------------

    knowledge_text = str(row.get("knowledge_areas", ""))

    if knowledge_text and knowledge_text != "nan":

        knowledge_mapping = {
            "computers and electronics": "Computer Systems",
            "telecommunications": "Networking",
            "programming": "Programming",
            "information technology": "Information Technology",
            "data analysis": "Data Analysis",
        }

        for item in knowledge_text.split(";"):

            item_lower = item.strip().lower()

            for key, normalized_skill in knowledge_mapping.items():

                if key in item_lower:
                    career_skills.add(normalized_skill)

    return sorted(career_skills)


def calculate_career_matches(proficiency):

    df = load_career_knowledge_base()

    career_matches = []

    for _, row in df.iterrows():

        career_skills = extract_career_skills(row)

        matched_skills = []
        missing_skills = []

        total_score = 0

        for skill in career_skills:

            student_level = proficiency.get(skill, 0)

            if student_level > 0:

                total_score += student_level / 5

                matched_skills.append(
                    f"{skill} ({student_level}/5)"
                )

            else:

                missing_skills.append(skill)

        if career_skills:

            match_percentage = (
                total_score / len(career_skills)
            ) * 100

        else:

            match_percentage = 0

        career_matches.append(
            {
                "career": row["career"],
                "onet_code": row["onet_code"],
                "description": row["description"],
                "match_percentage": round(
                    match_percentage,
                    1
                ),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "career_skills": career_skills,
            }
        )

    career_matches.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return career_matches

def calculate_projected_match(proficiency, target_career):
    """
    Calculate the projected match percentage for a specific career
    using hypothetical skill proficiency levels.
    """

    matches = calculate_career_matches(proficiency)

    for match in matches:
        if match["career"] == target_career:
            return match

    return None