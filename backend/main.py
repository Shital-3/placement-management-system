# ================= STANDARD LIBRARIES =================
import os
from datetime import datetime, timedelta

# ================= FASTAPI =================
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ================= DATABASE =================
from sqlalchemy.orm import Session
from backend.database import engine, SessionLocal
from backend import models

# ================= SCHEMAS =================
from backend.schemas import UserCreate, UserResponse, JobCreate, ApplicationCreate

# ================= AUTH =================
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

# ================= APP INIT =================
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= FILE STORAGE =================
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# ================= CREATE TABLES =================
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

# ================= DATABASE =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= AUTH DEPENDENCIES =================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_admin(user: models.User = Depends(get_current_user)):
    if user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user

def require_alumni(user: models.User = Depends(get_current_user)):
    if user.role.value != "alumni":
        raise HTTPException(status_code=403, detail="Alumni only")
    return user

# ================= LOGIN =================
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    token = create_access_token({
        "sub": user.email,
        "role": user.role.value
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role.value
    }

# ================= REGISTER =================
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# ================= ADMIN DASHBOARD =================
@app.get("/admin/dashboard")
def admin_dashboard(db: Session = Depends(get_db), user: models.User = Depends(require_admin)):
    return {
        "total_students": db.query(models.User).filter(models.User.role == models.UserRole.student).count(),
        "total_jobs": db.query(models.Job).count(),
        "total_applications": db.query(models.Application).count()
    }

# ================= ADMIN APPLICATIONS =================
@app.get("/admin/applications")
def get_applications(db: Session = Depends(get_db), user: models.User = Depends(require_admin)):
    apps = db.query(models.Application).all()
    result = []
    for application in apps:   # ✅ FIXED: was `for app in apps` which shadowed FastAPI app
        student = db.query(models.User).filter(models.User.id == application.student_id).first()
        job = db.query(models.Job).filter(models.Job.id == application.job_id).first()
        result.append({
            "id": application.id,
            "student_name": student.name if student else "N/A",
            "job_title": job.title if job else "N/A",
            "status": application.status.value
        })
    return result

# ================= UPDATE STATUS =================
@app.put("/admin/update-status/{app_id}")
def update_status(app_id: int, data: dict,
                  db: Session = Depends(get_db),
                  user: models.User = Depends(require_admin)):
    app_obj = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    app_obj.status = data.get("status").lower()
    db.commit()
    return {"message": "Status updated"}

# ================= POST JOB (ADMIN) =================
@app.post("/admin/post-job")
def post_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_admin)
):
    try:
        new_job = models.Job(
            title=job.title,
            description=job.description,
            location=job.location,
            salary=job.salary,
            deadline=job.deadline
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return {"message": "Job posted successfully"}
    except Exception as e:
        print("POST JOB ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to post job")

# ================= ADMIN JOBS =================
@app.get("/admin/jobs")
def get_admin_jobs(   # ✅ FIXED: was duplicate name `get_jobs`
    db: Session = Depends(get_db),
    user: models.User = Depends(require_admin)
):
    return db.query(models.Job).all()

# ================= STUDENT JOBS =================
@app.get("/student/jobs")
def get_student_jobs(   # ✅ FIXED: was duplicate name `get_jobs`
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    return db.query(models.Job).all()

# ================= APPLY JOB =================
@app.post("/student/apply")
def apply_job(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    new_app = models.Application(
        student_id=user.id,
        job_id=data.job_id,
        status="pending"
    )
    db.add(new_app)
    db.commit()
    return {"message": "Applied successfully"}

# ================= RESUME =================
@app.post("/alumni/upload-resume")
def upload_resume(file: UploadFile = File(...), title: str = Form(...),
                  db: Session = Depends(get_db),
                  user: models.User = Depends(require_alumni)):
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    resume = models.Resume(title=title, file_path=path, user_id=user.id)
    db.add(resume)
    db.commit()
    return {"msg": "Uploaded"}

@app.get("/alumni/resumes")
def get_resumes(db: Session = Depends(get_db),
                user: models.User = Depends(require_alumni)):
    data = db.query(models.Resume).filter(models.Resume.user_id == user.id).all()
    return [{"id": r.id, "title": r.title} for r in data]

@app.get("/alumni/resume/{id}")
def download_resume(id: int, db: Session = Depends(get_db),
                    user: models.User = Depends(require_alumni)):
    r = db.query(models.Resume).filter(models.Resume.id == id,
                                       models.Resume.user_id == user.id).first()
    if not r:
        raise HTTPException(404, "Not found")
    return FileResponse(r.file_path)

# ================= MATERIAL =================
@app.post("/alumni/upload-material")
def upload_material(file: UploadFile = File(...), title: str = Form(...),
                    db: Session = Depends(get_db),
                    user: models.User = Depends(require_alumni)):
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    m = models.Material(title=title, file_path=path, user_id=user.id)
    db.add(m)
    db.commit()
    return {"msg": "Uploaded"}

@app.get("/alumni/materials")
def get_materials(db: Session = Depends(get_db),
                  user: models.User = Depends(require_alumni)):
    data = db.query(models.Material).filter(models.Material.user_id == user.id).all()
    return [{"id": m.id, "title": m.title} for m in data]

@app.get("/alumni/material/{id}")
def download_material(id: int, db: Session = Depends(get_db),
                      user: models.User = Depends(require_alumni)):
    m = db.query(models.Material).filter(models.Material.id == id,
                                         models.Material.user_id == user.id).first()
    if not m:
        raise HTTPException(404, "Not found")
    return FileResponse(m.file_path)

# ================= ALUMNI APPLICATIONS =================
@app.get("/alumni/applications")
def alumni_applications(db: Session = Depends(get_db),
                         user: models.User = Depends(require_alumni)):
    return db.query(models.Application).filter(
        models.Application.student_id == user.id).all()

# ================= MENTORSHIP =================
@app.get("/alumni/mentorship-requests")
def mentorship(db: Session = Depends(get_db),
               user: models.User = Depends(require_alumni)):
    data = db.query(models.Mentorship).all()
    result = []
    for r in data:
        result.append({
            "id": r.id,
            "student_name": "Student",
            "status": r.status
        })
    return result

@app.post("/alumni/accept-mentorship/{id}")
def accept(id: int, db: Session = Depends(get_db),
           user: models.User = Depends(require_alumni)):
    r = db.query(models.Mentorship).filter(models.Mentorship.id == id).first()  # ✅ FIXED: deprecated .get()
    if not r:
        raise HTTPException(status_code=404, detail="Mentorship request not found")
    r.status = "accepted"
    r.alumni_id = user.id
    db.commit()
    return {"msg": "Accepted"}