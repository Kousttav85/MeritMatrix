import streamlit as st
import pandas as pd
import uuid
import requests
from src.algorithms import AutocompleteTrie, fuzzy_match, FieldGraph

st.set_page_config(page_title="MeritMatrix UI", layout="wide")

API_URL = "http://127.0.0.1:8000"

# 1. Sidebar Profile
st.sidebar.title("👤 Profile")
with st.sidebar.form("profile"):
    student = {
        "edu_level": st.selectbox("Level", ["Undergraduate", "Postgraduate", "PhD"]),
        "field": st.selectbox("Field", [
            "Agricultural Engineering", "Agricultural Sciences", "Machine Learning & AI",
            "Computer Science", "Data Science", "Environmental Science & Geospatial",
            "Environmental Engineering", "Ecology & Economics", "Engineering",
            "Basic Sciences", "Medicine", "Arts & Humanities", "Business & Management"
        ]),
        "cgpa": st.number_input("CGPA", value=8.0, step=0.1),
        "family_income": st.number_input("Annual Family Income (INR)", min_value=0, value=200000, step=50000),
        "gender": st.selectbox("Gender", ["Female", "Male", "Other"])
    }
    st.form_submit_button("Match")

# 2. Hidden Admin Access
st.sidebar.divider()
admin_password_input = st.sidebar.text_input("Admin Access", type="password")
is_admin = False
if "admin_password" in st.secrets:
    is_admin = (admin_password_input == st.secrets["admin_password"])

# 3. Fetch Data via API
@st.cache_data
def fetch_scholarships():
    try:
        res = requests.get(f"{API_URL}/scholarships")
        return res.json() if res.status_code == 200 else []
    except:
        return []

scholarships = fetch_scholarships()

@st.cache_resource
def build_search_structures(scholarships_data):
    trie = AutocompleteTrie()
    graph = FieldGraph()
    for sch in scholarships_data:
        for word in sch["title"].split():
            trie.insert(word)
    return trie, graph

trie, graph = build_search_structures(scholarships)

st.title("🎓 MeritMatrix")

if not scholarships:
    st.error("⚠️ Cannot connect to the API. Ensure Uvicorn is running on port 8000.")
    st.stop()

if is_admin:
    tabs = st.tabs(["Search Engine", "🛠️ Admin Dashboard"])
    tab_main, tab_admin = tabs[0], tabs[1]
else:
    tabs = st.tabs(["Search Engine"])
    tab_main = tabs[0]

with tab_main:
    query = st.text_input("🔍 Search", "")
    if query:
        suggestions = trie.get_suggestions(query)
        if suggestions:
            st.caption(f"*Suggestions:* {', '.join(suggestions[:5])}")
    st.divider()

    # Call API for matches
    try:
        match_res = requests.post(f"{API_URL}/match", json=student)
        api_matches = match_res.json() if match_res.status_code == 200 else []
    except:
        api_matches = []

    primary_matches = []
    matched_ids = {m["id"]: m for m in api_matches}

    student_field = student["field"]
    adjacent_fields = graph.get_adjacent_fields(student_field)
    recommended = []

    for sch in scholarships:
        if query and not fuzzy_match(query, sch["title"], threshold=2):
            continue

        if sch["id"] in matched_ids:
            score = matched_ids[sch["id"]]["score"]
            reasons = matched_ids[sch["id"]]["reasons"]
            primary_matches.append((sch, score, reasons))
        elif student_field not in sch["fields"] and any(adj in sch["fields"] for adj in adjacent_fields):
            recommended.append(sch)

    primary_matches = sorted(primary_matches, key=lambda x: x[1], reverse=True)

    for sch, score, reasons in primary_matches:
        with st.container(border=True):
            st.subheader(f"{sch['title']} ({score}% Match)")
            st.write(f"**Provider:** {sch['provider']} | **Deadline:** {sch['deadline']}")
            with st.expander("Eligibility Details"):
                for r in reasons:
                    st.write(r)

    if recommended and not query:
        st.subheader("🔗 Recommended Based on Adjacent Fields")
        st.info(f"Since you study **{student_field}**, you might be interested in these related disciplines:")
        for sch in recommended[:3]:
            with st.container(border=True):
                st.write(f"**{sch['title']}** — Targets: {', '.join(sch['fields'])}")

if is_admin:
    with tab_admin:
        st.subheader("Database Overview")
        st.dataframe(pd.DataFrame(scholarships), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Add Record")
            with st.form("add_form"):
                new_title = st.text_input("Title")
                new_provider = st.text_input("Provider")
                new_amount = st.text_input("Amount (e.g., ₹10,000)")
                if st.form_submit_button("Add Scholarship"):
                    new_data = {
                        "id": f"SCH_{uuid.uuid4().hex[:8].upper()}",
                        "title": new_title, "provider": new_provider, "amount": new_amount,
                        "deadline": "2026-12-31", "min_cgpa": 7.0, "max_income": 500000,
                        "education_levels": "Undergraduate", "fields": "All", "category": "All",
                        "gender": "All", "description": "Added via API admin.", "apply_link": "http://example.com"
                    }
                    requests.post(f"{API_URL}/admin/scholarships", json=new_data)
                    fetch_scholarships.clear()
                    st.rerun()

        with col2:
            st.subheader("Delete Record")
            del_id = st.text_input("Enter Scholarship ID to Delete")
            if st.button("Delete"):
                requests.delete(f"{API_URL}/admin/scholarships/{del_id}")
                fetch_scholarships.clear()
                st.rerun()