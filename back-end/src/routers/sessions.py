from fastapi import APIRouter , Depends ,HTTPException
from ..models import SessionRead , Session , StudentRead , TeacherRead,Payment,PaymentRead
from ..database import get_session
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
@router.patch("/finish/{id}")
def finish_session(id : int , session = Depends(get_session)):
    stmnt = select(SessionRead).where(SessionRead.id == id)
    ss = session.exec(stmnt).first()

    if not ss:
        raise HTTPException(404,"no session with given id!")
    
    ss.done = True
    session.add(ss)
    session.commit()
    session.refresh(ss)

    return ss
@router.patch("/unfinish/{id}")
def finish_session(id : int , session = Depends(get_session)):
    stmnt = select(SessionRead).where(SessionRead.id == id)
    ss = session.exec(stmnt).first()

    if not ss:
        raise HTTPException(404,"no session with given id!")
    
    ss.done = False
    session.add(ss)
    session.commit()
    session.refresh(ss)

    return ss

@router.patch("/pay/{id}")
def pay_session(id : int ,body:Payment , session = Depends(get_session)):
    stmnt = select(SessionRead).where(SessionRead.id == id)
    ss = session.exec(stmnt).first()

    if not ss:
        raise HTTPException(404,"no session with given id!")
    payment_contract = PaymentRead(
        amount = body.amount,
        date = body.date,
        teacher_id=body.teacher_id
    )

    session.add(payment_contract)
    session.commit()
    session.refresh(payment_contract)

    ss.payment_id = payment_contract.id
    session.add(ss)
    session.commit()
    session.refresh(ss)
    return ss

@router.patch("/unpay/{id}")
def unpay_session(id : int ,session = Depends(get_session)):
    stmnt = select(SessionRead).where(SessionRead.id == id)
    ss = session.exec(stmnt).first()

    if not ss:
        raise HTTPException(404,"no session with given id!")
    
    stmnt = select(PaymentRead).where(PaymentRead.id == ss.payment_id)
    contract = session.exec(stmnt).first() 

    if contract:
        ss.payment_id = None
        session.add(ss)
        session.delete(contract)
        session.commit()
    return {"status":"ok"}
    