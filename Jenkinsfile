pipeline {
    agent any

    environment {
        VERSION = '1.0.0'
        BACKEND_IMAGE = "employee-backend:${VERSION}"
        SWAGGER_PORT = '8001'
        GRAFANA_PORT = '8002'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Backend Tests') {
            steps {
                bat 'python -m pip install -r backend/requirements.txt'
                bat 'cd backend && python -m pytest -v'
            }
        }

        stage('Security Validation') {
            steps { bat 'python -m pip check' }
        }

        stage('Docker Build') {
            steps { bat 'docker build -t %BACKEND_IMAGE% backend' }
        }

        stage('Artifact Version') {
            steps {
                bat 'echo Build version: %VERSION%'
                bat 'type VERSION'
            }
        }

        stage('Kubernetes Backend Deploy') {
            steps {
                bat 'kubectl apply -f kubernetes/namespace.yaml'
                bat 'kubectl apply -f kubernetes/configmap.yaml'
                bat 'kubectl apply -f kubernetes/backend-deployment.yaml'
                bat 'kubectl apply -f kubernetes/backend-service.yaml'
                bat 'kubectl rollout status deployment/employee-backend -n employee-system --timeout=180s'
            }
        }

        stage('Backend Health and Metrics') {
            steps {
                bat 'kubectl get pods -n employee-system'
                bat 'kubectl get services -n employee-system'
                bat '''kubectl exec deployment/employee-backend -n employee-system -- python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())"'''
                bat '''kubectl exec deployment/employee-backend -n employee-system -- python -c "import urllib.request; print('METRICS OK'); print(urllib.request.urlopen('http://127.0.0.1:8000/metrics').read().decode()[:200])"'''
            }
        }

        stage('Deploy Prometheus') {
            steps {
                bat 'kubectl apply -f kubernetes/monitoring/namespace.yaml'
                bat 'kubectl apply -f kubernetes/monitoring/prometheus.yaml'
                bat 'kubectl rollout status deployment/prometheus -n monitoring --timeout=180s'
            }
        }

        stage('Deploy Grafana') {
            steps {
                bat 'kubectl apply -f kubernetes/monitoring/grafana.yaml'
                bat 'kubectl rollout status deployment/grafana -n monitoring --timeout=180s'
            }
        }

        stage('Monitoring Validation') {
            steps {
                bat 'kubectl get pods -n monitoring'
                bat 'kubectl get services -n monitoring'
                bat '''kubectl exec deployment/prometheus -n monitoring -- wget -qO- http://127.0.0.1:9090/-/ready'''
                bat '''kubectl exec deployment/grafana -n monitoring -- wget -qO- http://127.0.0.1:3000/api/health'''
            }
        }

        stage('Start Swagger and Grafana') {
            steps {
                bat '''
                    echo Starting Swagger...
                    set JENKINS_NODE_COOKIE=dontKillMe
                    start "" /B cmd /c "set JENKINS_NODE_COOKIE=dontKillMe&& kubectl port-forward service/employee-backend %SWAGGER_PORT%:8000 -n employee-system > swagger-port-forward.log 2>&1"

                    echo Starting Grafana...
                    start "" /B cmd /c "set JENKINS_NODE_COOKIE=dontKillMe&& kubectl port-forward service/grafana %GRAFANA_PORT%:3000 -n monitoring > grafana-port-forward.log 2>&1"

                    powershell -NoProfile -Command "Start-Sleep -Seconds 5"

                    echo ==========================================
                    echo EMPLOYEE MANAGEMENT SYSTEM
                    echo ==========================================
                    echo Swagger : http://localhost:8001/docs
                    echo Health  : http://localhost:8001/health
                    echo Metrics : http://localhost:8001/metrics
                    echo Grafana : http://localhost:8002
                    echo Login   : admin / admin
                    echo ==========================================
                    exit /b 0
                '''
            }
        }
    }

    post {
        always {
            echo 'Employee Management CI/CD + Monitoring pipeline completed.'
        }
        success {
            echo 'BUILD SUCCESS - Swagger: http://localhost:8001/docs | Grafana: http://localhost:8002'
        }
        failure {
            echo 'BUILD FAILED - Check the failed stage above.'
        }
    }
}
