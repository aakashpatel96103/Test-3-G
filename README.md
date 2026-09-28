# Employee Management System - Jenkins + Kubernetes + Prometheus + Grafana

Backend-only FastAPI project.

Jenkins automatically:
1. Checkout
2. Install dependencies
3. Run tests
4. Run pip check
5. Build Docker image
6. Deploy backend to Kubernetes
7. Validate health and metrics
8. Deploy Prometheus
9. Deploy Grafana
10. Validate monitoring
11. Start local port forwarding

URLs after a successful Jenkins build:
- Swagger: http://localhost:8001/docs
- Health: http://localhost:8001/health
- Metrics: http://localhost:8001/metrics
- Grafana: http://localhost:8002

Grafana login:
admin / admin

Prometheus is automatically configured as the Grafana data source.

This package intentionally contains no frontend.
