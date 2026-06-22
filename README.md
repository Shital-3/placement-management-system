# 🎓 Placement Management System

A role-based **Placement Management System** that streamlines campus recruitment activities by connecting **Students**, **Administrators**, and **Alumni** on a single platform. The system simplifies job posting, application tracking, resume management, alumni engagement, and secure user authentication through JWT-based role-based access control.

---

## 🚀 Features

### 👨‍🎓 Student Module

* Browse available job opportunities
* Apply for jobs online
* Upload and manage resumes
* Track application status in real-time
* Access alumni-shared resources

### 👨‍💼 Admin Module

* Create and manage job postings
* Review student applications
* Manage users and roles
* Monitor placement activities

### 🎓 Alumni Module

* Share placement preparation resources
* Provide mentorship opportunities
* Engage with students
* Post career-related updates

### 🔐 Security Features

* JWT Authentication
* Role-Based Access Control (RBAC)
* Protected API Endpoints
* Secure User Sessions

---

## 🛠️ Tech Stack

| Category         | Technology              |
| ---------------- | ----------------------- |
| Backend          | FastAPI                 |
| Language         | Python                  |
| Database         | MySQL                   |
| ORM              | SQLAlchemy              |
| Authentication   | JWT (JSON Web Tokens)   |
| Frontend         | HTML5, CSS3, JavaScript |
| API Architecture | REST API                |

---

## 📂 Project Structure

```bash
placement-management-system/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── auth/
│   │   ├── utils/
│   │   └── database.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── student/
│   ├── admin/
│   ├── alumni/
│   ├── assets/
│   └── index.html
│
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.9+
* MySQL Server
* Git
* pip

---

### Clone Repository

```bash
git clone https://github.com/your-username/placement-management-system.git
cd placement-management-system
```

---

### Backend Setup

Create and activate a virtual environment:

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file inside the backend directory:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/placement_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### Database Setup

Create the database:

```sql
CREATE DATABASE placement_db;
```

Run migrations or create tables:

```bash
python -m app.database
```

---

### Run Backend Server

```bash
uvicorn backend.app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Run Frontend

```bash
cd frontend
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

---

## 🔐 User Roles

| Role    | Permissions                                            |
| ------- | ------------------------------------------------------ |
| Student | Browse jobs, apply, upload resumes, track applications |
| Admin   | Manage jobs, users, and applications                   |
| Alumni  | Share resources, mentorship opportunities, and updates |

---

## 📡 REST API Endpoints

| Endpoint                       | Method | Description          | Access        |
| ------------------------------ | ------ | -------------------- | ------------- |
| `/auth/register`               | POST   | Register user        | Public        |
| `/auth/login`                  | POST   | Login user           | Public        |
| `/jobs/`                       | GET    | View all jobs        | Authenticated |
| `/jobs/`                       | POST   | Create job posting   | Admin         |
| `/applications/apply/{job_id}` | POST   | Apply for job        | Student       |
| `/applications/my`             | GET    | View my applications | Student       |
| `/resume/upload`               | POST   | Upload resume        | Student       |
| `/alumni/resources`            | GET    | View resources       | Authenticated |
| `/alumni/resources`            | POST   | Add resource         | Alumni        |

---

## 🎯 Key Highlights

* Role-Based Dashboard System
* JWT Authentication & Authorization
* Resume Upload Functionality
* RESTful API Architecture
* Alumni Mentorship Platform
* Responsive User Interface
* Modular Backend Design

---

## 🔮 Future Enhancements

* Email Notifications
* SMS Alerts
* Resume Parsing
* AI-Based Skill Matching
* Placement Analytics Dashboard
* Alumni-Student Chat System


---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

##

---

##
