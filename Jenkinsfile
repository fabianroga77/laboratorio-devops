// =============================================================================
// Jenkinsfile — Pipeline CD (Entrega Continua) del microservicio Core Banking Lite
//
// Cumple los stages exigidos por la actividad:
//   1. Clonar el repositorio
//   2. Construir la imagen Docker
//   3. Publicar la imagen en un registro (DockerHub)
//
// El CI (build + tests) vive en GitHub Actions (.github/workflows/ci.yml).
// Este pipeline se encarga del CD: empaquetar y publicar el artefacto desplegable.
//
// Requisitos en Jenkins:
//   - Credencial tipo "Username with password" con ID 'dockerhub-credentials'
//   - Docker disponible en el agente (Docker Pipeline plugin)
// =============================================================================


pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'fabianroga77'
        IMAGE_NAME     = "${DOCKERHUB_USER}/mi-microservicio"
        IMAGE_TAG      = "build-${env.BUILD_NUMBER}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Clonar repositorio') {
            steps {
                echo "Repositorio obtenido por Jenkins SCM"

                script {
                    env.GIT_SHA = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()

                    echo "Commit desplegado: ${env.GIT_SHA}"
                }
            }
        }       

        stage('Pruebas de humo') {
            steps {
                echo "Ejecutando smoke tests de la API antes de construir la imagen..."

                sh '''
                    cat > smoke_test.py <<'PYEOF'
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# El servicio responde y está sano
health = client.get("/health")

assert health.status_code == 200, health.text
assert health.json()["status"] == "ok"

# Los datos seed cargan correctamente
clientes = client.get("/api/v1/clientes")

assert clientes.status_code == 200, clientes.text
assert clientes.json()["total"] >= 2

print("Smoke tests OK")
PYEOF

                    docker run --rm \
                        -v "$PWD:/workspace" \
                        -w /workspace \
                        python:3.11-slim \
                        bash -c "
                            python --version &&
                            python -m venv .venv &&
                            .venv/bin/pip install --quiet --upgrade pip &&
                            .venv/bin/pip install --quiet -r requirements.txt &&
                            .venv/bin/python -c 'import sys; sys.path.insert(0, \"app\"); exec(open(\"smoke_test.py\").read())'
                        "
                '''
            }
        }

        stage('Construir imagen Docker') {
            steps {
                echo "Construyendo la imagen ${IMAGE_NAME}:${IMAGE_TAG}..."

                sh """
                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        -t ${IMAGE_NAME}:${GIT_SHA} \
                        -t ${IMAGE_NAME}:latest \
                        .
                """
            }
        }

        stage('Publicar en DockerHub') {
            steps {
                echo "Publicando la imagen en DockerHub..."

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh """
                        echo "\$DOCKER_PASS" | docker login \
                            -u "\$DOCKER_USER" \
                            --password-stdin

                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:${GIT_SHA}
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }
    }

    post {
        success {
            echo "CD completado. Imagen publicada: ${IMAGE_NAME}:${IMAGE_TAG} (commit ${GIT_SHA})"
        }

        failure {
            echo "El pipeline de CD falló. Revisar los logs del stage correspondiente."
        }

        always {
            sh 'docker logout || true'

            sh """
                docker rmi \
                    ${IMAGE_NAME}:${IMAGE_TAG} \
                    ${IMAGE_NAME}:${GIT_SHA} \
                    ${IMAGE_NAME}:latest \
                    || true
            """
        }
    }
}