
# from typing import List , Optional
from sqlmodel import SQLModel , create_engine , Field

from typing import Optional
from sqlmodel import SQLModel , create_engine , Field
from datetime import datetime 
from enum import Enum


class Teacher(SQLModel):
    name : str
    password : str = None
    

class TeacherRead(Teacher , table = True):
    id : Optional[int] = Field(default=None , primary_key=True) 
class Student(SQLModel):
    username : str

class StudentRead(Student, table = True):
    id : Optional[int] = Field(default=None , primary_key=True)

class Payment(SQLModel):  
    amount: float
    date: datetime # Corrected name and inherited from SQLModel
    teacher_id : str = Field (foreign_key="teacherread.id")
    currency : str = "MAD"

class PaymentRead(Payment , table=True):
    id : Optional[int] = Field(default=None , primary_key=True)

class Session(SQLModel):
    teacher_id : int = Field (foreign_key="teacherread.id")
    student_id : int = Field(foreign_key="studentread.id")
    payment_id : Optional[int] = Field(default=None, foreign_key="paymentread.id")

class SessionRead(Session , table = True):
    id : Optional[int] = Field(default=None , primary_key=True)



class Admin(SQLModel ,table=True):
    id:int = Field(default=None , primary_key=True)
    username : str 
    photo_url : str | None 
    password : str
    transactions : int = 0
    token : str

