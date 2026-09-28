pipeline {
    agent any

    environment {
        APP_NAME = 'employee-backend'
        NAMESPACE = 'employee-system'
        IMAGE = 'employee-backend:2.0.0'
        MONITORING_NAMESPACE = 'monitoring'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Clean Existing Backend') {
            steps {
                bat '''
                    kubectl delete deployment %APP_NAME% -n %NAMESPACE% --ignore-not-found=true --wait=true
                    kubectl delete service %APP_NAME% -n %NAMESPACE% --ignore-not-found=true
                    kubectl delete pod -l app=%APP_NAME% -n %NAMESPACE% --ignore-not-found=true --wait=true
                    powershell -NoProfile -Command "Start-Sleep -Seconds 3"
                '''
            }
        }

        stage('Clean Existing Monitoring') {
            steps {
                bat '''
                    kubectl delete deployment prometheus -n %MONITORING_NAMESPACE% --ignore-not-found=true --wait=true
                    kubectl delete deployment grafana -n %MONITORING_NAMESPACE% --ignore-not-found=true --wait=true
                    kubectl delete service prometheus -n %MONITORING_NAMESPACE% --ignore-not-found=true
                    kubectl delete service grafana -n %MONITORING_NAMESPACE% --ignore-not-found=true
                    kubectl delete pod -l app=prometheus -n %MONITORING_NAMESPACE% --ignore-not-found=true --wait=true
                    kubectl delete pod -l app=grafana -n %MONITORING_NAMESPACE% --ignore-not-found=true --wait=true
                '''
            }
        }

        stage('Clean Docker Image') {
            steps { bat 'docker rmi -f %IMAGE% 2>nul || exit /b 0' }
        }

        stage('Install Dependencies') {
            steps { bat 'python -m pip install -r backend/requirements.txt' }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    cd backend
                    python -m pytest tests -v
                '''
            }
        }

        stage('Dependency Validation') {
            steps { bat 'python -m pip check' }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    docker build --no-cache -t %IMAGE% backend
                    docker image inspect %IMAGE% >nul
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat '''
                    docker run --rm %IMAGE% python --version
                    docker run --rm %IMAGE% python -c "from app.main import app; assert any(r.path == '/health' for r in app.routes); assert any(r.path == '/metrics' for r in app.routes); print('APPLICATION ROUTES OK')"
                    docker run --rm %IMAGE% python -c "import prometheus_client, prometheus_fastapi_instrumentator; print('PROMETHEUS PACKAGES OK')"
                '''
            }
        }

        stage('Prepare Kubernetes') {
            steps {
                bat '''
                    kubectl apply -f kubernetes/namespace.yaml
                    kubectl apply -f kubernetes/monitoring/namespace.yaml
                    if exist kubernetes/configmap.yaml kubectl apply -f kubernetes/configmap.yaml
                '''
            }
        }

        stage('Load Image Into Kubernetes') {
            steps {
                bat '''
                    for /f "delims=" %%C in ('kubectl config current-context') do (
                        echo Kubernetes context: %%C
                        if /I "%%C"=="minikube" minikube image load %IMAGE%
                        if /I "%%C"=="kind-kind" kind load docker-image %IMAGE%
                    )
                    docker image inspect %IMAGE% >nul
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Deploy Backend') {
            steps {
                bat '''
                    kubectl apply -f kubernetes/backend-deployment.yaml
                    kubectl apply -f kubernetes/backend-service.yaml
                    kubectl rollout status deployment/%APP_NAME% -n %NAMESPACE% --timeout=180s
                '''
            }
        }

        stage('Verify Backend') {
            steps {
                bat '''
                    kubectl get deployment %APP_NAME% -n %NAMESPACE%
                    kubectl get pods -n %NAMESPACE% -o wide
                    kubectl get service %APP_NAME% -n %NAMESPACE%
                    kubectl exec deployment/%APP_NAME% -n %NAMESPACE% -- python --version
                    kubectl exec deployment/%APP_NAME% -n %NAMESPACE% -- python -c "from app.main import app; assert any(r.path == '/metrics' for r in app.routes); print('ROUTE CHECK OK')"
                '''
            }
        }

        stage('Health Check') {
            steps {
                bat '''
                    kubectl exec deployment/%APP_NAME% -n %NAMESPACE% -- python -c "import urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8000/health'); assert r.status == 200; print(r.read().decode())"
                '''
            }
        }

        stage('Metrics Check') {
            steps {
                bat '''
                    kubectl exec deployment/%APP_NAME% -n %NAMESPACE% -- python -c "import urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8000/metrics'); assert r.status == 200; print('METRICS OK'); print(r.read().decode()[:1000])"
                '''
            }
        }

        stage('Deploy Prometheus') {
            steps {
                bat '''
                    kubectl apply -f kubernetes/monitoring/prometheus.yaml
                    kubectl rollout status deployment/prometheus -n %MONITORING_NAMESPACE% --timeout=180s
                '''
            }
        }

        stage('Deploy Grafana') {
            steps {
                bat '''
                    kubectl apply -f kubernetes/monitoring/grafana.yaml
                    kubectl rollout status deployment/grafana -n %MONITORING_NAMESPACE% --timeout=180s
                '''
            }
        }

        stage('Monitoring Validation') {
            steps {
                bat '''
                    kubectl get pods -n %MONITORING_NAMESPACE%
                    kubectl get services -n %MONITORING_NAMESPACE%
                    kubectl exec deployment/prometheus -n %MONITORING_NAMESPACE% -- wget -qO- http://127.0.0.1:9090/-/ready
                    kubectl exec deployment/grafana -n %MONITORING_NAMESPACE% -- wget -qO- http://127.0.0.1:3000/api/health
                '''
            }
        }

        stage('Start Services') {
            steps {
                bat '''
                    set JENKINS_NODE_COOKIE=dontKillMe
                    start "" /B cmd /c "set JENKINS_NODE_COOKIE=dontKillMe&& kubectl port-forward service/employee-backend 8001:8000 -n employee-system > swagger-port-forward.log 2>&1"
                    start "" /B cmd /c "set JENKINS_NODE_COOKIE=dontKillMe&& kubectl port-forward service/grafana 8002:3000 -n monitoring > grafana-port-forward.log 2>&1"
                    powershell -NoProfile -Command "Start-Sleep -Seconds 5"
                '''
            }
        }
    }

    post {
        success { echo 'BUILD SUCCESS' }
        failure { echo 'BUILD FAILED' }
    }
}