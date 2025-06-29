

A FastAPI-based RESTful backend for managing tasks with support for full CRUD operations, filtering, sorting, and searching.

---

### 🚀 Features

- ✅ Task creation, reading, updating, and deletion (CRUD)
    
- 🔍 Filtering by status, priority, and assignee
    
- 🧾 Searching in title and description
    
- 🔃 Sorting by any field (e.g., due date, title, priority)
    
- 📄 Automatic OpenAPI (Swagger) documentation
    
- 📦 SQLite with SQLModel ORM
    
- 🔐 Validation with Pydantic
    

---

### 🛠️ Tech Stack

- **Python 3.9+**
    
- **FastAPI**
    
- **SQLModel** (built on SQLAlchemy + Pydantic)
    
- **SQLite** (local database)
    
- **Uvicorn** (ASGI server)
    

---

### 🧰 Installation & Setup

#### 1. Clone the repo

```bash
git clone https://github.com/your-username/task-api.git
cd task-api
```

#### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run the API

```bash
uvicorn main:app --reload
```

#### 5. Access Docs

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
    

---

### 🔐 Assumptions & Design Decisions

- SQLite is used for simplicity and portability.
    
- SQLModel is chosen for its tight integration with FastAPI and Pydantic.
    
- Filtering via query parameters for `GET /tasks`, and advanced filtering via `POST /tasks/filter`.
    
- Seed data is inserted on first run unless the table is already populated.
    
- OpenAPI documentation is enabled by default for easy testing.
    

---

### 📬 Example API Calls

#### 🔹 Create Task

**POST** `/tasks`

```json
{
  "title": "New Task",
  "description": "Do something important",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-07-10T23:59:00",
  "assigned_to": "Ahmed"
}
```

#### 🔹 Get All Tasks

**GET** `/tasks?priority=high&search=important&sort_by=due_date&order=asc`

---

### 🧪 Testing Instructions

1. Run the app:
    

```bash
uvicorn main:app --reload
```

2. Use Postman, curl, or Swagger UI to interact with endpoints.
    

Example:

```bash
curl -X POST "http://127.0.0.1:8000/tasks" -H "Content-Type: application/json" -d "{\"title\":\"Sample Task\",\"priority\":\"low\"}"
```

---

### 📂 Folder Structure

```
.
├── main.py
├── models/
│   └── task.py
├── schemas/
│   └── task.py
│   └── task_filter.py
├── crud/
│   └── task.py
├── routers/
│   └── task_router.py
├── database.py
├── requirements.txt
└── README.md
```

---

