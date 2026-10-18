from fastapi import FastAPI,HTTPException,Path,Query
from sqlalchemy import create_engine ,String,select
from sqlalchemy.orm import sessionmaker , DeclarativeBase , Mapped ,mapped_column
from pydantic import BaseModel , Field ,EmailStr
from dotenv import load_dotenv
import os