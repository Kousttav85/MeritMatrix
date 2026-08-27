from datetime import datetime, date

def calculate_match_score(student: dict, scholarship: dict) -> tuple[int, list[str]]:
    reasons = []
    score = 100
    hard_disqualified = False

    # Deadline check
    deadline_date = datetime.strptime(scholarship["deadline"], "%Y-%m-%d").date()
    if deadline_date < date.today():
        return 0, ["❌ Deadline has passed"]

    # Gender check
    if scholarship["gender"] != "All" and student["gender"] != scholarship["gender"]:
        hard_disqualified = True
        reasons.append(f"❌ Restricted to {scholarship['gender']} applicants")

    # Education Level check
    if "All" not in scholarship["education_levels"] and student["edu_level"] not in scholarship["education_levels"]:
        hard_disqualified = True
        reasons.append(f"❌ Requires level: {', '.join(scholarship['education_levels'])}")

    # Field check
    if "All" not in scholarship["fields"] and student["field"] not in scholarship["fields"]:
        score -= 40
        reasons.append(f"⚠️ Target fields: {', '.join(scholarship['fields'])}")
    else:
        reasons.append("✅ Field of study matches")

    # CGPA & Income (Simplified for brevity)
    if student["cgpa"] < scholarship["min_cgpa"]:
        score -= 35
        reasons.append(f"⚠️ Requires min CGPA {scholarship['min_cgpa']}")
    
    if student["family_income"] > scholarship["max_income"]:
        score -= 30
        reasons.append("⚠️ Income ceiling exceeded")

    if hard_disqualified:
        return 0, reasons

    return max(0, score), reasons