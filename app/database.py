from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from pathlib import Path
import os

# Get the TESTING_MODE environment variable
# This is set by pytest in pyproject.toml
# It is true when running pytest, false otherwise
TESTING_MODE = os.environ.get("TESTING_MODE", "false") == "true"

SCRIPT_DIR = Path(__file__).parent.absolute()

REAL_DATABASE_PATH = SCRIPT_DIR / "tasks.db"
TEST_DATABASE_PATH = SCRIPT_DIR / "test_tasks.db"

REAL_DATABASE_URL = f"sqlite:///{REAL_DATABASE_PATH}"
TEST_DATABASE_URL = f"sqlite:///{TEST_DATABASE_PATH}"

if TESTING_MODE:
    DATABASE_URL = TEST_DATABASE_URL
else:
    DATABASE_URL = REAL_DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


Base.metadata.create_all(bind=engine)
