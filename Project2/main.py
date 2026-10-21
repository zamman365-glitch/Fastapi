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

class StudentCreate(BaseModel):
    name :str = Field(min_length=2, max_length=100) 
    email :EmailStr 
    course : str =Field(min_length=2, max_length=50) 

class StudentResponse(BaseModel):
    id:int
    name :str = Field(min_length=2, max_length=100) 
    email :EmailStr 
    course : str =Field(min_length=2, max_length=50) 

class StudentUpdate(BaseModel):
    name :str|None = Field(default=None, min_length=2, max_length=100) 
    email :EmailStr|None=Field(default=None) 
    course : str =Field(default=None, min_length=2, max_length=50)


@app.post("/students",response_model=StudentResponse)
def create_student(student_data :StudentCreate):
    db = SessionLocal()
    try:
        query = select(Student).where(Student.email == student_data.email)
        result = db.execute(query)
        existing_student = result.scalar_one_or_none()
        if existing_student:
            raise HTTPException(status_code=400, detail="Student with this email already exists")
        
        new_student = Student(
            name = student_data.name,
            email= student_data.email,
            course = student_data.course
            )
        db.add(new_student)
        db.commit()
        db.refresh(new_student) 
        return new_student
    finally:
        db.close()
        