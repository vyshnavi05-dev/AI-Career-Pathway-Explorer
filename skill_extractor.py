SKILLS = [
    # Programming
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",

    # Web & Database
    "SQL",
    "HTML",
    "CSS",

    # Systems & Cloud
    "Linux",
    "Windows",
    "Git",
    "Docker",
    "AWS",
    "Azure",

    # Networking & Security
    "Networking",
    "Cybersecurity",
    "Network Security",
    "Wireshark",
    "Nmap",
    "SIEM",
    "Splunk",
    "Incident Response",
    "Threat Analysis",
    "Log Analysis",
    "Ethical Hacking",
    "Penetration Testing",
    "Digital Forensics",

    # Data & AI
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "Scikit-learn",
    "Statistics",

    # Other
    "Excel",
    "Communication",
    "Leadership"
]

def extract_skills(resume_text):
    found_skills = []

    resume_text_lower = resume_text.lower()

    for skill in SKILLS:
        if skill.lower() in resume_text_lower:
            found_skills.append(skill)

    return found_skills