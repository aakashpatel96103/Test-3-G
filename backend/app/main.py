from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Employee Management System", version="2.0.0")

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Employee Management API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/employees")
def get_employees():
    return []

@app.post("/employees")
def create_employee(employee: dict):
    return {"message": "Employee created", "employee": employee}

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    return {"id": employee_id}

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: dict):
    return {"message": "Employee updated", "id": employee_id, "employee": employee}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    return {"message": "Employee deleted", "id": employee_id}