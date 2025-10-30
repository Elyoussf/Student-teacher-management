

from fastapi import APIRouter , Depends ,HTTPException
from ..models import Student,StudentRead
from ..database import get_session
from  ..utils.random_string import generate_random_string
from sqlmodel import select 
router = APIRouter(
    prefix="/students",       
    tags=["Students"]         
)

lengthofpassword = 25
@router.post("/create")
async def create_student(body :Student, session = Depends(get_session)):
    new_student = StudentRead(
        username = body.username
    )
    session.add(new_student)
    session.commit()
    session.refresh(new_student)
    return new_student



@router.patch("/{id}")
async def update_student(id : int ,body:Student , session = Depends(get_session)):
    stmt = select(StudentRead).where(StudentRead.id == id)
    res = session.exec(stmt).first()
    if not res:
        raise HTTPException(404 , "No Student found with given id!")
    if body.username:
        res.username = body.username
    
    session.add(res)
    session.commit()
    session.refresh(res)

    return res

@router.delete("/delete/{id}")
async def delete_teacher(id : str,session = Depends(get_session)):
    student = session.exec(select(StudentRead).where(StudentRead.id == id)).first()

    if not student:
        raise HTTPException(404 , "No Student found with given id!")
    
    session.delete(student)
    session.commit()
    return {"status" : "ok"}


@router.get("/{id}")
def get_data(id : int,session = Depends(get_session)):
    student = session.exec(select(StudentRead).where(StudentRead.id == id)).first()
    if not student:
        raise HTTPException(404 , "Not found!")
    return student
