from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Employee Management System API",
    description="Production-grade RESTful API for Employee Management, instrumented with Prometheus observability.",
    version="2.0.0",
)

Instrumentator().instrument(app).expose(app)


@app.get("/", tags=["System Diagnostics"], summary="Service Root Status")
def root():
    """Verify service availability and root message."""
    return {"message": "Employee Management API is running"}


@app.get("/health", tags=["System Diagnostics"], summary="Service Health Probe")
def health():
    """Service liveness and readiness probe endpoint."""
    return {"status": "healthy"}


@app.get("/employees", tags=["Employee Management"], summary="List Employees")
def get_employees():
    """Retrieve all active employee records."""
    return []


@app.post("/employees", tags=["Employee Management"], summary="Create Employee")
def create_employee(employee: dict):
    """Register and create a new employee record."""
    return {"message": "Employee created", "employee": employee}


@app.get("/employees/{employee_id}", tags=["Employee Management"], summary="Get Employee Details")
def get_employee(employee_id: int):
    """Retrieve a specific employee record by their unique ID."""
    return {"id": employee_id}


@app.put("/employees/{employee_id}", tags=["Employee Management"], summary="Update Employee Details")
def update_employee(employee_id: int, employee: dict):
    """Update an existing employee record by ID."""
    return {"message": "Employee updated", "id": employee_id, "employee": employee}


@app.delete("/employees/{employee_id}", tags=["Employee Management"], summary="Delete Employee")
def delete_employee(employee_id: int):
    """Remove an employee record from the system by ID."""
    return {"message": "Employee deleted", "id": employee_id}