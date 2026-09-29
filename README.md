# Employee Management System

A cloud-native, containerized RESTful API for Employee Management built with FastAPI, orchestrated on Kubernetes, monitored with Prometheus and Grafana, and automated through a Jenkins CI/CD pipeline.

---

## Architecture Overview

- **Backend Application**: FastAPI REST API exposing employee management endpoints and Prometheus metrics (`/metrics`).
- **Containerization**: Docker lightweight Python base image with dynamic semantic and build-tagged versioning.
- **Orchestration**: Kubernetes cluster running the application in the `employee-system` namespace with liveness and readiness health checks.
- **Monitoring & Observability**:
  - **Prometheus** (deployed in `monitoring` namespace) continuously scrapes API telemetry every 15s.
  - **Grafana** (deployed in `monitoring` namespace) auto-provisions custom dashboards displaying real user request rates, latency, status distributions, and system resource utilization.
- **Continuous Integration & Delivery (CI/CD)**: Jenkins Declarative Pipeline automating testing, dependency validation, container building, Kubernetes deployment rollout, and service verification.

---

## Project File Structure

```text
employee-management-system-jenkins-grafana/
├── backend/                                # FastAPI backend root directory
│   ├── app/                                # Application package
│   │   ├── __init__.py                     # Application package marker
│   │   └── main.py                         # REST API endpoints & Prometheus instrumentation
│   ├── tests/                              # Automated test suite
│   │   ├── __init__.py                     # Test suite package marker
│   │   └── test_main.py                    # Unit & integration test cases
│   ├── Dockerfile                          # Container image build specification
│   └── requirements.txt                    # Python application dependencies
├── kubernetes/                             # Kubernetes orchestration manifests
│   ├── namespace.yaml                      # Application namespace (employee-system)
│   ├── backend-deployment.yaml             # Deployment configuration with health probes
│   ├── backend-service.yaml                # ClusterIP service definition
│   └── monitoring/                         # Observability stack manifests
│       ├── namespace.yaml                  # Monitoring namespace
│       ├── prometheus.yaml                 # Prometheus deployment, ConfigMap & service
│       └── grafana.yaml                    # Grafana deployment, datasource & provisioned dashboard
├── .gitignore                              # Git exclusion patterns
├── Jenkinsfile                             # Declarative Jenkins CI/CD pipeline
├── README.md                               # Project documentation & operations guide
└── VERSION                                 # Semantic application version
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root service availability check |
| `GET` | `/health` | Health probe (liveness/readiness) |
| `GET` | `/metrics` | Prometheus metrics exposition |
| `GET` | `/employees` | Retrieve employee list |
| `POST` | `/employees` | Create a new employee |
| `GET` | `/employees/{employee_id}` | Retrieve employee by ID |
| `PUT` | `/employees/{employee_id}` | Update employee by ID |
| `DELETE` | `/employees/{employee_id}` | Delete employee by ID |
| `GET` | `/docs` | Interactive Swagger API documentation |
| `GET` | `/redoc` | ReDoc API documentation |

---

## CI/CD Pipeline Workflow

The Jenkins pipeline ([Jenkinsfile](./Jenkinsfile)) executes the following stages:

1. **Checkout**: Pulls the latest source code from SCM.
2. **Generate Image Tag**: Generates a unique build version tag (`v${BUILD_NUMBER}-${HASH}`).
3. **Clean Existing Resources**: Cleans up previous deployments, services, and pods.
4. **Install Dependencies**: Installs Python requirements.
5. **Run Tests**: Executes unit test suite using `pytest`.
6. **Dependency Validation**: Validates dependencies via `pip check`.
7. **Build Docker Image**: Builds the Docker container image without cache and tags it.
8. **Verify Docker Image**: Validates image runtime, routes, and Prometheus libraries.
9. **Prepare Kubernetes**: Configures namespaces (`employee-system` and `monitoring`).
10. **Load Image Into Kubernetes**: Loads the container image into the local cluster node.
11. **Deploy Backend**: Deploys the FastAPI service with rolling update verification.
12. **Verify Backend**: Validates pod status, connectivity, and route configuration.
13. **Health & Metrics Checks**: Verifies `/health` and `/metrics` response statuses.
14. **Deploy Prometheus & Grafana**: Deploys Prometheus and Grafana with automated provisioning.
15. **Monitoring Validation**: Verifies readiness of monitoring services.
16. **Start Services**: Establishes background port-forwarding for Swagger UI and Grafana.

---

## Service Endpoints & Access

After a successful deployment rollout:

| Service | URL | Credentials |
|---|---|---|
| **Swagger UI** | [http://localhost:8001/docs](http://localhost:8001/docs) | None |
| **Health Check** | [http://localhost:8001/health](http://localhost:8001/health) | None |
| **Prometheus Metrics** | [http://localhost:8001/metrics](http://localhost:8001/metrics) | None |
| **Grafana Dashboard** | [http://localhost:8002](http://localhost:8002) | `admin` / `admin` |

---

## Prerequisites

- **Docker Desktop** (with Kubernetes enabled)
- **kubectl** CLI
- **Jenkins** (with Pipeline and Git plugins)
- **Python 3.12+**
- **Git**