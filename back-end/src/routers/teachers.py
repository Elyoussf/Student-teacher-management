from fastapi import APIRouter , Depends ,HTTPException
from ..models import Teacher , TeacherRead  , StudentRead, SessionRead
from ..database import get_session
from  ..utils.random_string import generate_random_string
from sqlmodel import select 
router = APIRouter(
    prefix="/teachers",       
    tags=["Teachers"]         
)

lengthofpassword = 25
@router.post("/create")
async def create_teacher(body :Teacher, session = Depends(get_session)):
    statement = select(TeacherRead).where(TeacherRead.name == body.name and TeacherRead.password == body.password)
    result = session.exec(statement)
    if result.first():
        # there is a teacher with the same name and proposed password
        raise HTTPException(409 , "A Teacher with the same details found")
    if body.password == None:
        body.password = generate_random_string(lengthofpassword)
    
    newteacherdb= TeacherRead(
        name = body.name,
        password=body.password
    )
     
    session.add(newteacherdb)
    session.commit()
    session.refresh(newteacherdb)
    return newteacherdb

@router.get("/")
async def get_all(session = Depends(get_session)):
    statement = select(TeacherRead)
    res = session.exec(statement)
    to_send = []
    for t in res.all():
        obj = {
            "name" : t.name,
            "id" : t.id
        }
        to_send.append(obj)
    return to_send

@router.get("/{id}")
async def get_students_sessions_by_id(id : str , session = Depends(get_session)):
    stmnt = select(SessionRead).join(StudentRead, SessionRead.student_id == StudentRead.id).where(SessionRead.teacher_id == id)
    res = session.exec(stmnt)
    return res.all()

@router.patch("/update/{id}")
async def update_teacher(id : int ,body:Teacher , session = Depends(get_session)):
    stmt = select(TeacherRead).where(TeacherRead.id == id)

    res = session.exec(stmt).first()

    if not res:
        raise HTTPException(404 , "No Teacher found with given id!")
    
    if body.name:
        res.name = body.name
    if body.password:
        res.password = body.password
    
    session.add(res)
    session.commit()
    session.refresh(res)

    return body

@router.delete("/delete/{id}")
async def delete_teacher(id : int,session = Depends(get_session)):
    teacher = session.exec(select(TeacherRead).where(TeacherRead.id == id))

    if not teacher:
        raise HTTPException(404 , "No Teacher found with given id!")
    
    session.delete(teacher.first())
    session.commit()
    return {"status" : "ok"}



