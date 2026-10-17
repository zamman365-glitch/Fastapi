from fastapi import FastAPI
from sqlalchemy import create_engine ,String,select
from sqlalchemy.orm import sessionmaker , DeclarativeBase , Mapped ,mapped_column
from pydantic import BaseModel , Field ,EmailStr

DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_CeFVas2fX4jB@ep-autumn-sun-b3ltou01-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(50), unique=True)
    course:Mapped[str] = mapped_column(String(100))
    
app = FastAPI()

Base.metadata.create_all(bind=engine)


class StudentCreate(BaseModel):
    name :str = Field(min_length=2, max_length=100) 
    email :EmailStr 
    course : str =Field(min_length=2, max_length=50) 

class StudentResponse(BaseModel):
    id:int
    name :str = Field(min_length=2, max_length=100) 
    email :EmailStr 
    course : str =Field(min_length=2, max_length=50) 

@app.post("/students",response_model=StudentResponse)
def create_student(student_data :StudentCreate):
    db = SessionLocal()
    try:
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
        
@app.get("/students/",response_model=list[StudentResponse])
def get_all_student():
    db= SessionLocal()
    try:
        query = select(Student)
        print(f"Query: {query}")
        result = db.execute(query)
        students = result.scalars().all()
        return students
    finally:
        db.close()