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