from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ================= DATABASE URL =================
# Update password, host, port, and database name as per your MySQL setup
DATABASE_URL = "mysql+pymysql://root:Shital%402003@localhost/placement_system"

# ================= ENGINE =================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False
)

# ================= SESSION =================
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ================= BASE CLASS =================
Base = declarative_base()