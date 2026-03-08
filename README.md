# NLP Applied to Emotion Detection
### NLP4EMAI · Natural Language Processing for EMAI

> **How to get the materials**
> - **No Git experience?** Click any **Download ↓** link below — you get a ZIP with everything for that session.
> - **Know Git?** `git clone` this repo once, then `git pull` before each session to get new files automatically.

---

## Course materials

| Session | Topic | Slides and Activities | Solutions |
|---------|-------|:---------------------:|:---------:|
| **Session 1** | Introduction to NLP & Emotion Detection | [Download ↓](../../releases/tag/session1-start) | — |
| **Session 2** | Text as Data: Preprocessing & Normalisation | - | - |
| **Session 3** | Numeric Representations: BoW & TF-IDF | — | — |

> 🔒 Sessions not yet available show — instead of a link.  
> Solutions are released **after** each session.  
> Session 1 is a slides-only session — no activity files.

---

## What is in each session folder

```
session1/
└── slides.pdf                         ← no activity files for this session

session2/
├── slides.pdf
├── reviews.csv                        ← keep this in the same folder as the scripts
└── activities/
    ├── activity_1_student.py          ← hand-made pipeline (TODOs 1–13)
    ├── activity_1_student.ipynb
    ├── activity_2_student.py          ← pandas pipeline (TODOs 1–8)
    ├── activity_2_student.ipynb
    └── solutions/                     ← released after the session
        ├── activity_1_solution.py
        ├── activity_1_solution.ipynb
        ├── activity_2_solution.py
        └── activity_2_solution.ipynb

session3/
└── ...                                ← coming soon
```

---

## Setup (Session 2 onwards)

```bash
# 1. Clone the repo (once, at the start of the course)
git clone https://github.com/YOUR_USERNAME/nlp4emai.git
cd nlp4emai

# 2. Install dependencies
pip install pandas jupyter

# 3. Before each session, pull the latest files
git pull
```

If you are using **Google Colab**, upload the `.ipynb` file directly and also upload `reviews.csv` to the same Colab session before running any cells.

---

*Course materials · Not for redistribution outside the programme.*
