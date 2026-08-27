import sqlite3
from pathlib import Path

DB_PATH = Path("data/scholarships.db")
DB_PATH.parent.mkdir(exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scholarships (
            id TEXT PRIMARY KEY,
            title TEXT,
            provider TEXT,
            amount TEXT,
            deadline TEXT,
            min_cgpa REAL,
            max_income INTEGER,
            education_levels TEXT,
            fields TEXT,
            category TEXT,
            gender TEXT,
            description TEXT,
            apply_link TEXT
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM scholarships')
    if cursor.fetchone()[0] == 0:
        seed_data = [
            ("SCH_IN_001", "AICTE GATE Scholarship", "All India Council for Technical Education", "₹12,400 / month", "2026-12-31", 0.0, 9999999, "Postgraduate", "Engineering,Agricultural Engineering,Computer Science", "All", "All", "Stipend for GATE-qualified students admitted to M.Tech programs.", "https://pgscholarship.aicte-india.org/"),
            
            ("SCH_IN_002", "Swami Vivekananda Merit-Cum-Means Scholarship", "Govt. of West Bengal", "₹5,000 / month", "2026-11-30", 6.0, 250000, "Undergraduate,Postgraduate", "Engineering,Agricultural Engineering,Computer Science", "Economically Weaker Section", "All", "State scholarship for meritorious students domiciled in West Bengal.", "https://svmcm.wb.gov.in/"),
            
            ("SCH_IN_003", "DST INSPIRE Fellowship", "Department of Science and Technology", "₹37,000 / month + HRA", "2026-10-15", 7.0, 9999999, "PhD", "Basic Sciences,Agricultural Sciences,Medicine", "All", "All", "Doctoral fellowship for university toppers pursuing research in science and agriculture.", "https://online-inspire.gov.in/"),
            
            ("SCH_IN_004", "ICAR National Talent Scholarship (NTS)", "Indian Council of Agricultural Research", "₹3,000 / month", "2026-09-30", 7.0, 9999999, "Undergraduate", "Agricultural Sciences,Agricultural Engineering", "All", "All", "For students pursuing agriculture degrees outside their state of domicile via AIEE.", "https://www.myscheme.gov.in/schemes/nts-ug"),
            
            ("SCH_IN_005", "Google Generation Scholarship", "Google", "₹2,00,000 one-time", "2026-12-01", 7.5, 9999999, "Undergraduate,Postgraduate", "Computer Science,Machine Learning & AI,Engineering", "All", "Female", "Supporting women pursuing degrees in computer science and technology.", "https://buildyourfuture.withgoogle.com/scholarships")
        ]
        cursor.executemany('''
            INSERT INTO scholarships VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_data)
        conn.commit()
    conn.close()

def get_all_scholarships() -> list[dict]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scholarships')
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        d = dict(row)
        d["education_levels"] = d["education_levels"].split(",")
        d["fields"] = d["fields"].split(",")
        results.append(d)
    return results

def add_scholarship_record(data_tuple):
    """Inserts a new scholarship into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO scholarships VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data_tuple)
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Handles duplicate ID gracefully
    finally:
        conn.close()

def delete_scholarship_record(sch_id):
    """Deletes a scholarship by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM scholarships WHERE id = ?', (sch_id,))
    conn.commit()
    conn.close()