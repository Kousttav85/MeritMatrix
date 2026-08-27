# 🎓 MeritMatrix

MeritMatrix is a high-performance, microservice-based scholarship matching engine. It leverages advanced data structures and a strict API-driven architecture to dynamically connect students with relevant financial aid and fellowships based on their academic profiles.

##  Key Features

- **Microservice Architecture:** Fully decoupled **FastAPI** backend and **Streamlit** frontend.
- **Algorithmic Matching:** Utilizes a **Trie** data structure for lightning-fast autocomplete and Dynamic Programming (**DP**) for fuzzy-matched search queries.
- **Graph Recommendations:** Implements a localized **FieldGraph** to suggest adjacent academic disciplines.
- **Secure Admin Panel:** Hidden UI dashboard for full CRUD (Create, Read, Update, Delete) operations on the SQLite database.
- **Automated CI/CD:** Integrated **GitHub Actions** workflow running a rigorous **PyTest** suite on every push.

##  Tech Stack

- **Backend:** FastAPI, Pydantic, Uvicorn
- **Frontend:** Streamlit, Pandas, Requests
- **Database:** SQLite3
- **DevOps:** GitHub Actions, PyTest

## 💻 Local Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Kousttav85/MeritMatrix.git](https://github.com/Kousttav85/MeritMatrix.git)
cd MeritMatrix

```

### 2. Create the Virtual Environment & Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create a .streamlit folder in the root directory, and inside it, create a secrets.toml file with your admin password:
```bash
admin_password = "YourSecurePassword123!"
```

### 4. Run the Microservices
You will need two terminal windows to run the frontend and backend simultaneously.

Terminal 1 (Backend API):

```Bash
uvicorn src.api:app --reload
```
The API and interactive Swagger UI docs will be available at http://127.0.0.1:8000/docs

Terminal 2 (Frontend UI):

```Bash
streamlit run app.py
```
The user interface will be available at http://localhost:8501