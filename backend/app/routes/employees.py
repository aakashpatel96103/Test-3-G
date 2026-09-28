from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Employee
from ..schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    item = db.query(Employee).filter(Employee.id == employee_id).first()
    if not item:
        raise HTTPException(404, "Employee not found")
    return item

@router.post("", response_model=EmployeeResponse)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(Employee).filter(Employee.email == data.email).first():
        raise HTTPException(400, "Email already exists")
    item = Employee(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db)):
    item = db.query(Employee).filter(Employee.id == employee_id).first()
    if not item:
        raise HTTPException(404, "Employee not found")
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    item = db.query(Employee).filter(Employee.id == employee_id).first()
    if not item:
        raise HTTPException(404, "Employee not found")
    db.delete(item)
    db.commit()
    return {"message": "Employee deleted successfully"}
