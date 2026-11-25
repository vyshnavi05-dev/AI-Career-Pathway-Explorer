import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# File locations
# ---------------------------------------------------------

DATA_DIR = Path("onet_data")

occupation_file = DATA_DIR / "occupation_data.csv"
essential_skills_file = DATA_DIR / "essential_skills.csv"
knowledge_file = DATA_DIR / "knowledge.csv"
software_file = DATA_DIR / "software_skills.csv"

output_file = "career_knowledge_base.csv"


# ---------------------------------------------------------
# Load O*NET data
# ---------------------------------------------------------

print("📂 Loading O*NET data...")

occupations = pd.read_csv(occupation_file)
essential = pd.read_csv(essential_skills_file)
knowledge = pd.read_csv(knowledge_file)
software = pd.read_csv(software_file)

print("✅ O*NET files loaded!")


# ---------------------------------------------------------
# Select relevant CS / IT occupations
# ---------------------------------------------------------

# We want the prototype to cover multiple computer-science
# and IT career areas, not only cybersecurity.

relevant_keywords = [

    # Software development
    "software developer",
    "software engineer",
    "computer programmer",
    "application developer",
    "web developer",
    "web administrator",

    # Computer systems / IT
    "computer systems",
    "information systems",
    "information technology",
    "computer systems analyst",
    "computer support",
    "computer user support",
    "computer network support",

    # Networking
    "computer network",
    "network administrator",
    "network engineer",
    "network architect",
    "network and computer systems",

    # Cybersecurity
    "information security",
    "cybersecurity",
    "cyber security",
    "computer security",
    "security engineer",
    "security architect",
    "security operations",

    # Digital forensics
    "digital forensics",
    "computer forensics",
    "forensic computer",

    # Database
    "database administrator",
    "database architect",
    "database developer",

    # Data / AI / ML
    "data scientist",
    "machine learning",
    "artificial intelligence",
    "computer and information research",
    "data mining",

    # Cloud / infrastructure
    "cloud",
    "systems administrator",
    "system administrator",
    "systems engineer",

    # Programming / computing research
    "computer research",
    "computer scientist",

    # IT project / architecture roles
    "computer systems architect",
    "information systems manager"
]


def is_relevant(title):
    """
    Check whether an O*NET occupation belongs to
    a CS / IT related career area.
    """

    title_lower = title.lower()

    return any(
        keyword in title_lower
        for keyword in relevant_keywords
    )


relevant_occupations = occupations[
    occupations["Title"].apply(is_relevant)
].copy()


# ---------------------------------------------------------
# Remove obviously unrelated occupations
# ---------------------------------------------------------

# Some titles may contain technology-related words while
# still belonging to a different field.

exclude_keywords = [
    "sales",
    "marketing",
    "financial",
    "finance",
    "accounting",
    "credit",
    "logistics",
    "medical",
    "health",
    "clinical",
    "legal",
    "law",
    "insurance",
    "human resources",
    "hr",

    # Engineering fields outside the CS / IT scope
    "geographic information systems",
    "microsystems",
    "nanosystems",
    "solar energy"
]

def is_not_excluded(title):
    title_lower = title.lower()

    return not any(
        keyword in title_lower
        for keyword in exclude_keywords
    )


relevant_occupations = relevant_occupations[
    relevant_occupations["Title"].apply(is_not_excluded)
].copy()


print(
    f"🎯 Relevant CS / IT occupations selected: "
    f"{len(relevant_occupations)}"
)


# ---------------------------------------------------------
# Process each occupation
# ---------------------------------------------------------

career_data = []


for _, occupation in relevant_occupations.iterrows():

    code = occupation["O*NET-SOC Code"]
    title = occupation["Title"]
    description = occupation["Description"]


    # -----------------------------------------------------
    # Essential skills
    # -----------------------------------------------------

    skill_rows = essential[
        (essential["O*NET-SOC Code"] == code)
        &
        (essential["Scale ID"] == "IM")
    ]

    skill_rows = skill_rows[
        skill_rows["Data Value"] >= 3.0
    ]

    essential_skills = skill_rows[
        "Element Name"
    ].tolist()


    # -----------------------------------------------------
    # Knowledge areas
    # -----------------------------------------------------

    knowledge_rows = knowledge[
        (knowledge["O*NET-SOC Code"] == code)
        &
        (knowledge["Scale ID"] == "IM")
    ]

    knowledge_rows = knowledge_rows[
        knowledge_rows["Data Value"] >= 3.0
    ]

    knowledge_areas = knowledge_rows[
        "Element Name"
    ].tolist()


    # -----------------------------------------------------
    # Software / technologies
    # -----------------------------------------------------

    software_rows = software[
        software["O*NET-SOC Code"] == code
    ]

    software_names = software_rows[
        "Workplace Example"
    ].dropna().unique().tolist()


    # -----------------------------------------------------
    # Create career record
    # -----------------------------------------------------

    career_data.append(
        {
            "career": title,
            "onet_code": code,
            "description": description,
            "essential_skills": "; ".join(
                essential_skills
            ),
            "knowledge_areas": "; ".join(
                knowledge_areas
            ),
            "software_skills": "; ".join(
                software_names
            ),
            "source": "O*NET 31.0"
        }
    )


# ---------------------------------------------------------
# Create final knowledge base
# ---------------------------------------------------------

career_knowledge_base = pd.DataFrame(
    career_data
)


career_knowledge_base.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

print("\n🎉 Career knowledge base created!")

print(
    f"📄 File: {output_file}"
)

print(
    f"📊 Number of occupations: "
    f"{len(career_knowledge_base)}"
)


# ---------------------------------------------------------
# Show selected careers
# ---------------------------------------------------------

print("\n💻 Selected CS / IT careers:")

for career in career_knowledge_base["career"]:
    print("   •", career)


print("\n🔎 Preview:")

print(
    career_knowledge_base[
        [
            "career",
            "onet_code",
            "essential_skills",
            "knowledge_areas",
            "software_skills"
        ]
    ]
    .head(5)
    .to_string(index=False)
)


print("\n✅ O*NET preprocessing complete!")