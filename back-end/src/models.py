
# from typing import List , Optional
from sqlmodel import SQLModel , create_engine , Field

from typing import Optional
from sqlmodel import SQLModel , create_engine , Field
from datetime import datetime 


class Teacher(SQLModel):
    name : str
    password : str
    
class TeacherRead(Teacher , table = True):
    id : Optional[str] = Field(default=None , primary_key=True) # Assuming UUIDs (str)

class Student(SQLModel):
    username : str

class StudentRead(Student, table = True):
    id : Optional[str] = Field(default=None , primary_key=True)

class Payment(SQLModel): # Corrected name and inherited from SQLModel
    amount: float
    date: datetime # Use datetime.datetime or similar
    # to is good, but for consistency, maybe teacher_id
    teacher_id : str = Field (foreign_key="teacherread.id")
    currency : str = "MAD"

class PaymentRead(Payment , table=True):
    id : Optional[str] = Field(default=None , primary_key=True)

class Session(SQLModel):
    teacher_id : str = Field (foreign_key="teacherread.id")
    student_id : str = Field(foreign_key="studentread.id")
    
    payment_id : Optional[str] = Field(default=None, foreign_key="paymentread.id")

class SessionRead(Session , table = True):
    id : Optional[str] = Field(default=None , primary_key=True)



class Admin(SQLModel):
    username : str 
    photo_url : str | None 
    password : str
    transactions : int = 0

class AdminRead(Admin , table = True):
    id:str = Field(default=None , primary_key=True)

    
