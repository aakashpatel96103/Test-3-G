# Employee Management System - Strict CI/CD Fix v2

Backend-only FastAPI application.

Pipeline:
Git checkout -> clean old Kubernetes resources -> install dependencies -> pytest -> pip check -> Docker build -> Docker verification -> Kubernetes namespaces -> image availability -> backend deployment -> health -> metrics -> Prometheus -> Grafana -> monitoring validation -> port forwarding.

Required:
- Jenkins
- Git
- Python
- Docker Desktop
- Kubernetes enabled in Docker Desktop
- kubectl

URLs after successful build:
- Swagger: http://localhost:8001/docs
- Health: http://localhost:8001/health
- Metrics: http://localhost:8001/metrics
- Grafana: http://localhost:8002

Grafana login:
admin / admin

The missing kubernetes/namespace.yaml from the previous build is included in this package.