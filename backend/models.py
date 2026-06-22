from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
import enum


# ================= USER ROLE ENUM =================
class UserRole(enum.Enum):
    student = "student"
    admin = "admin"
    alumni = "alumni"


# ================= ENUM FOR APPLICATION STATUS =================
class ApplicationStatus(enum.Enum):
    Pending = "Pending"
    Shortlisted = "Shortlisted"
    Rejected = "Rejected"
    Selected = "Selected"


# ================= USER MODEL =================
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.student)

    applications = relationship("Application", back_populates="student")
    resumes = relationship("Resume", back_populates="user")
    materials = relationship("Material", back_populates="user")


# ================= JOB MODEL =================
class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    location = Column(String(100))
    salary = Column(String(50))
    deadline = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())

    applications = relationship("Application", back_populates="job")


# ================= APPLICATION MODEL =================
class Application(Base):
    __tablename__ = "applications"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    resume_path = Column(String(255), nullable=True)

    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.Pending)

    applied_at = Column(TIMESTAMP, server_default=func.now())

    interview_date = Column(Date, nullable=True)
    interview_time = Column(String(20), nullable=True)
    interview_mode = Column(String(50), nullable=True)
    interview_notes = Column(Text, nullable=True)

    student = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")


# ================= RESUME MODEL =================
class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    file_path = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="resumes")


# ================= MATERIAL MODEL =================
class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    file_path = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="materials")


# ================= MENTORSHIP MODEL =================
class Mentorship(Base):
    __tablename__ = "mentorship"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    alumni_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    status = Column(String(50), default="pending")  # ✅ FIXED (no MySQL error)