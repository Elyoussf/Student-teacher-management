from fastapi import APIRouter , Depends ,HTTPException
from ..models import SessionRead , Session , StudentRead , TeacherRead
from ..database import get_session
from  ..utils.random_string import generate_random_string
from sqlmodel import select 
router = APIRouter(
    prefix="/sessions",       
    tags=["Sessions"]         
)


@router.post("/create")
async def create_session(body : Session,num:int,session = Depends(get_session)):
    teacher_id = body.teacher_id
    student_id = body.student_id

    student = session.exec(select(StudentRead).where(StudentRead.id == student_id)).first()
    if not student:
        raise HTTPException(404 , "Student Not found Contact the developper Hamza _-_")
    teacher = session.exec(select(TeacherRead).where(TeacherRead.id == teacher_id)).first()

    if not teacher:
        raise HTTPException(404 , "Teacher Not found Contact the developper Hamza _-_")

    # suppose num >=1 validated by frontend
    for _ in range(num):
        new_session = SessionRead(
            teacher_id = teacher_id,
            student_id = student_id,
            payment_id = None
        )
        session.add(new_session)
    session.commit()
    return {"status":"done"}

    