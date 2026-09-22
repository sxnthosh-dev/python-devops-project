pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Environment') {
            steps {
                withCredentials([
                    file(credentialsId: 'kimai-env', variable: 'ENV_FILE'),
                    file(credentialsId: 'grafana-ini', variable: 'GRAFANA_INI')
                ]) {
                    sh '''
                        cp "$ENV_FILE" .env
                        chmod 600 .env

                        mkdir -p grafana
                        cp "$GRAFANA_INI" grafana/grafana.ini
                        chmod 600 grafana/grafana.ini

                        echo "Environment and Grafana configuration prepared"
                    '''
                }
            }
        }

        stage('Validate Docker Compose') {
            steps {
                sh '''
                    docker compose -p python-devops-project config > /dev/null
                    echo "Docker Compose configuration is valid"
                '''
            }
        }

        stage('Pull Docker Images') {
            steps {
                sh '''
                    docker compose -p python-devops-project pull
                '''
            }
        }

        stage('Deploy Kimai Stack') {
            steps {
                sh '''
                    docker compose -p python-devops-project up -d
                '''
            }
        }

        stage('Show Container Status') {
            steps {
                sh '''
                    docker compose -p python-devops-project ps
                '''
            }
        }

        stage('Wait for Kimai') {
            steps {
                sh '''
                    for i in {1..30}; do
                        if curl --fail --silent --show-error \
                            --location \
                            --output /dev/null \
                            http://127.0.0.1:8000/en/homepage; then

                            echo "Kimai is responding"
                            exit 0
                        fi

                        echo "Waiting for Kimai..."
                        sleep 5
                    done

                    echo "Kimai failed to become ready"

                    docker compose -p python-devops-project ps

                    docker compose -p python-devops-project logs \
                        --tail=100 kimai

                    exit 1
                '''
            }
        }

        stage('Verify Kimai Health') {
            steps {
                sh '''
                    status=$(docker inspect \
                        --format='{{.State.Health.Status}}' \
                        kimai_app)

                    echo "Kimai health status: $status"

                    if [ "$status" != "healthy" ]; then
                        echo "Kimai container is not healthy"
                        docker inspect kimai_app
                        exit 1
                    fi
                '''
            }
        }

        stage('Verify MariaDB Health') {
            steps {
                sh '''
                    status=$(docker inspect \
                        --format='{{.State.Health.Status}}' \
                        devops-mariadb)

                    echo "MariaDB health status: $status"

                    if [ "$status" != "healthy" ]; then
                        echo "MariaDB container is not healthy"
                        docker inspect devops-mariadb
                        exit 1
                    fi
                '''
            }
        }

        stage('Verify Prometheus') {
            steps {
                sh '''
                    curl --fail --silent --show-error \
                        http://127.0.0.1:9090/-/healthy

                    echo
                    echo "Prometheus is healthy"
                '''
            }
        }

        stage('Verify Grafana') {
            steps {
                sh '''
                    curl --fail --silent --show-error \
                        --location \
                        --output /dev/null \
                        http://127.0.0.1:3000/login

                    echo "Grafana is reachable"
                '''
            }
        }

        stage('Deployment Summary') {
            steps {
                sh '''
                    echo "======================================"
                    echo "Kimai CI/CD deployment successful"
                    echo "======================================"

                    docker compose -p python-devops-project ps
                '''
            }
        }
    }

    post {
        always {
            sh '''
                rm -f .env
                rm -f grafana/grafana.ini
            '''
        }

        success {
            echo 'CI/CD pipeline completed successfully.'
        }

        failure {
            echo 'CI/CD pipeline failed.'
        }
    }
}