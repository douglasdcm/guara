## 🎓 Education Platform CLI (Guará-Based)

This project is a **CLI-based education management platform** built using the **Guará framework**, following a use-case-driven architecture where **business scenarios, implementation, and tests are unified**. Instead of separating requirements from code, the system models behavior through **transactions and executable scenarios**, making the application highly readable, maintainable, and aligned with business rules.

The platform supports core academic operations such as:

* Student and course creation
* Subject management
* Enrollment in courses and subjects
* Grade assignment and GPA calculation

All interactions are performed via **command-line interface (CLI)**, and the system persists data using **SQLite**.

---

## 🧠 Architecture Approach

This project leverages Guará’s philosophy:

* **Use cases are code**
* **Transactions represent user actions**
* **Assertions validate business behavior**

This ensures a single source of truth across:

* Requirements
* Implementation
* Testing

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo>
```

### 2. Create a virtual environment (recommended)

```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

Make sure you have a `requirements.txt` file, then run:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the CLI

Example commands:

```bash
python main.py --action create_student --name John
python main.py --action create_course --name Math
python main.py --action create_subject --name Algebra --course C1
python main.py --action enroll_course --student S1 --course C1
python main.py --action enroll_subject --student S1 --subject SUB1
python main.py --action set_grade --student S1 --subject SUB1 --grade 8
python main.py --action gpa --student S1
```

---

## 🧪 Running Tests

Tests are also written using Guará scenarios:

```bash
pytest
```

---

## 📚 Documentation

* Guará Documentation: [https://guara.readthedocs.io/en/latest/](https://guara.readthedocs.io/en/latest/)
* Modeling Guide: [https://guara.readthedocs.io/en/latest/MODELING.html](https://guara.readthedocs.io/en/latest/MODELING.html)
* [Businness Requirements](REQUIREMENTS.md)

---

## 💡 Key Benefits

* Single source of truth for requirements and implementation
* High readability with business-oriented syntax
* Faster development and testing cycles
* Strong alignment between technical and business perspectives

---

## 📌 Notes

* The system uses SQLite (`education.db`) for persistence
* All operations are CLI-based (no UI)
* Designed for extensibility with new transactions and scenarios

---

## 🚀 Final Thought

With Guará, your **use cases become your architecture**.
