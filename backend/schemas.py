from pydantic import BaseModel
from datetime import date
from typing import Optional


# ================= USER =================

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


# ================= TOKEN =================

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


# ================= JOB =================

class JobCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    deadline: Optional[date] = None


class JobResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    location: Optional[str]
    salary: Optional[str]
    deadline: Optional[date]

    class Config:
        from_attributes = True


# ================= APPLICATION =================

class ApplicationCreate(BaseModel):
    job_id: int


# ================= PASSWORD CHANGE =================

class ChangePassword(BaseModel):
    old_password: str
    new_password: str


# ================= STATUS UPDATE =================

class UpdateApplicationStatus(BaseModel):
    status: str