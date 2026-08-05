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
        // Cambiar <usuario-dockerhub> por el usuario real de DockerHub
        DOCKERHUB_USER = 'fabianroga77'
        IMAGE_NAME     = "${DOCKERHUB_USER}/mi-microservicio"
        // Tag basado en el número de build de Jenkins + short SHA del commit
        IMAGE_TAG      = "build-${env.BUILD_NUMBER}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        // --- Stage 1: Clonar el repositorio ---
        stage('Clonar repositorio') {
            steps {
                echo "Clonando el repositorio del microservicio..."
                git branch: 'main',
                    url: 'https://github.com/fabianroga77/mi-microservicio.git'
                script {
                    // Capturamos el SHA corto para etiquetar la imagen de forma trazable
                    env.GIT_SHA = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    echo "Commit desplegado: ${env.GIT_SHA}"
                }
            }
        }

        // --- Stage 2: Pruebas rápidas antes de empaquetar (buena práctica) ---
        stage('Pruebas de humo') {
            steps {
                echo "Ejecutando smoke tests de la API antes de construir la imagen..."
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --quiet -r requirements.txt
                    cd app
                    python - <<'EOF'
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
EOF
                '''
            }
        }

        // --- Stage 3: Construir la imagen Docker ---
        stage('Construir imagen Docker') {
            steps {
                echo "Construyendo la imagen ${IMAGE_NAME}:${IMAGE_TAG}..."
                script {
                    // Etiquetamos con el número de build y con el SHA del commit
                    sh """
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} \
                                     -t ${IMAGE_NAME}:${GIT_SHA} \
                                     -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }

        // --- Stage 4: Publicar la imagen en DockerHub ---
        stage('Publicar en DockerHub') {
            steps {
                echo "Publicando la imagen en DockerHub..."
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ''' + "${IMAGE_NAME}:${IMAGE_TAG}" + '''
                        docker push ''' + "${IMAGE_NAME}:${GIT_SHA}" + '''
                        docker push ''' + "${IMAGE_NAME}:latest" + '''
                    '''
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
            // Limpieza: cerramos sesión de Docker y borramos imágenes locales del build
            sh 'docker logout || true'
            sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:${GIT_SHA} ${IMAGE_NAME}:latest || true"
        }
    }
}
