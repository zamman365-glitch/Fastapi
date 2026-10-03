
from fastapi import FastAPI
import json

app = FastAPI() 


def load_students():
    with open("students.json", "r") as file:
        return json.load(file)

def save_students(students):
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)    


@app.get("/")
def Hello():
    return {"message" : "Hello FastAPI"}



@app.get("/students")
def get_students():
    return load_students()



@app.get("/students/{student_id}")
def get_student(student_id: int):
    students = load_students()  
    for student in students:
        if student["id"] == student_id:
            return student
    return {"message": "Student not found"}




@app.post("/students")
def create_student(new_student:dict):
    students = load_students()
    students.append(new_student)
    save_students(students)
    return new_student



@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: dict):
    students = load_students()
    for student in students:
        if student["id"] == student_id:
            student.update(updated_student)
            save_students(students)
            return student
    return {"message": "Student not found"}



@app.delete("/students/{student_id}")
def delete_student(student_id : int):
    students = load_students()
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_students(students)
            return {"message": "Student deleted"}
    return {"message": "Student not found"}