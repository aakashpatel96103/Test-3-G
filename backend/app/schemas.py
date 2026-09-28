from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    role: str

class EmployeeUpdate(EmployeeCreate):
    pass

class EmployeeResponse(EmployeeCreate):
    id: int
    class Config:
        from_attributes = True
