from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Employee Management System API",
    description="Production-grade RESTful API for Employee Management, instrumented with Prometheus observability.",
    version="2.0.0",
)

Instrumentator().instrument(app).expose(app)


@app.get("/", summary="Root Endpoint")
def root():
    """Verify service availability."""
    return {"message": "Employee Management API is running"}


@app.get("/health", summary="Service Health Check")
def health():
    """Service liveness and readiness probe endpoint."""
    return {"status": "healthy"}


@app.get("/employees", summary="List Employees")
def get_employees():
    """Retrieve all employee records."""
    return []


@app.post("/employees", summary="Create Employee")
def create_employee(employee: dict):
    """Create a new employee record."""
    return {"message": "Employee created", "employee": employee}


@app.get("/employees/{employee_id}", summary="Get Employee Details")
def get_employee(employee_id: int):
    """Retrieve a specific employee record by ID."""
    return {"id": employee_id}


@app.put("/employees/{employee_id}", summary="Update Employee Details")
def update_employee(employee_id: int, employee: dict):
    """Update an existing employee record by ID."""
    return {"message": "Employee updated", "id": employee_id, "employee": employee}


@app.delete("/employees/{employee_id}", summary="Delete Employee")
def delete_employee(employee_id: int):
    """Delete an employee record by ID."""
    return {"message": "Employee deleted", "id": employee_id}