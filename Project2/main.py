from fastapi import FastAPI,HTTPException,Path,Query
from sqlalchemy import create_engine ,String,select
from sqlalchemy.orm import sessionmaker , DeclarativeBase , Mapped ,mapped_column
from pydantic import BaseModel , Field ,EmailStr
from dotenv import load_dotenv
import os


DATABASE_URL=" "
class Student(Base):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    course: Mapped[str] = mapped_column(String(50), nullable=False)