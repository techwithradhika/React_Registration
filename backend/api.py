from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/Registration"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Register(Base):
    __tablename__ = 'Register'

    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False)
    DateOfBirth = Column(String(10))

class RegisterCreate(BaseModel):
    Name: str
    Email: str
    DateOfBirth: str

class RegisterResponse(BaseModel):
    ID: int
    Name: str
    Email: str
    DateOfBirth: str

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/", response_model=RegisterResponse)
def create_register(register: RegisterCreate, db: Session = Depends(get_db)):
    try:
        try:
            date_of_birth = datetime.strptime(register.DateOfBirth, "%d/%m/%Y").date()
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Please provide the date in the format 'DD/MM/YYYY'.")

        db_register = Register(Name=register.Name, Email=register.Email, DateOfBirth=date_of_birth)
        db.add(db_register)
        db.commit()
        db.refresh(db_register)
        db_register_dict = db_register.__dict__.copy()
        db_register_dict["DateOfBirth"] = register.DateOfBirth
        return RegisterResponse(**db_register_dict)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
@app.get("/register/", response_model=List[RegisterResponse])
def read_all_registers(db: Session = Depends(get_db)):
    registers = db.query(Register).all()
    register_list = []
    for register in registers:
        register_dict = register.__dict__.copy()
        register_dict["DateOfBirth"] = str(register_dict["DateOfBirth"])
        register_list.append(RegisterResponse(**register_dict))
    return register_list

@app.get("/register/{register_id}/", response_model=RegisterResponse)
def read_register(register_id: int, db: Session = Depends(get_db)):
    db_register = db.query(Register).filter(Register.ID == register_id).first()
    if db_register is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Register not found")
    
    db_register_dict = db_register.__dict__.copy()
    db_register_dict["DateOfBirth"] = str(db_register_dict["DateOfBirth"])
    return RegisterResponse(**db_register_dict) 

@app.put("/register/{register_id}/", response_model=RegisterResponse)
def update_register(register_id: int, register: RegisterCreate, db: Session = Depends(get_db)):
    try:
        db_register = db.query(Register).filter(Register.ID == register_id).first()
        if db_register is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Register not found")
        
        try:
            date_of_birth = datetime.strptime(register.DateOfBirth, "%d/%m/%Y").date()
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Please provide the date in the format 'DD/MM/YYYY'.")

        db_register.Name = register.Name
        db_register.Email = register.Email
        db_register.DateOfBirth = date_of_birth
        db.commit()
        db.refresh(db_register)
        db_register_dict = db_register.__dict__.copy()
        db_register_dict["DateOfBirth"] = register.DateOfBirth
        return RegisterResponse(**db_register_dict)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

@app.delete("/register/{register_id}/", response_model=RegisterResponse)
def delete_register(register_id: int, db: Session = Depends(get_db)):
    try:
        db_register = db.query(Register).filter(Register.ID == register_id).first()
        if db_register is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Register not found")
        
        db.delete(db_register)
        db.commit()
        db_register_dict = db_register.__dict__.copy()
        db_register_dict["DateOfBirth"] = str(db_register_dict["DateOfBirth"])
        return RegisterResponse(**db_register_dict)    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
