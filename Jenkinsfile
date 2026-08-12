// =============================================================================
// Jenkinsfile — Pipeline CD (Entrega Continua) del microservicio Core Banking Lite
//
// Cumple los stages exigidos por la actividad:
//   1. Clonar el repositorio
//   2. Construir la imagen Docker
//   3. Publicar la imagen en un registro (DockerHub)
//
// El CI (tests + validacion) vive en GitHub Actions (.github/workflows/ci.yml).
// Este pipeline se encarga del CD: empaquetar y publicar el artefacto desplegable.
//
// Requisitos en el agente de Jenkins:
//   - Docker disponible (Docker Pipeline plugin)
//   - Credencial "Username with password" con ID 'dockerhub-credentials'
//     (usuario de DockerHub + un Access Token)
// =============================================================================

pipeline {
    agent any

    environment {
        // Usuario de DockerHub. La imagen se publica como <usuario>/laboratorio-devops
        DOCKERHUB_USER = 'fabianrojas77'
        IMAGE_NAME     = "${DOCKERHUB_USER}/laboratorio-devops"
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
                    url: 'https://github.com/fabianroga77/laboratorio-devops.git'
                script {
                    env.GIT_SHA = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    echo "Commit desplegado: ${env.GIT_SHA}"
                }
            }
        }

        // --- Stage 2: Construir la imagen Docker ---
        stage('Construir imagen Docker') {
            steps {
                echo "Construyendo la imagen ${IMAGE_NAME}:${IMAGE_TAG}..."
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} \\
                                 -t ${IMAGE_NAME}:${GIT_SHA} \\
                                 -t ${IMAGE_NAME}:latest .
                """
            }
        }

        // --- Stage 3: Prueba de humo sobre la imagen ya construida ---
        // No requiere Python en el agente: levanta el contenedor y consulta /health.
        stage('Prueba de humo') {
            steps {
                echo "Verificando que el contenedor responde en /health..."
                sh """
                    docker run -d --rm --name smoke_test -p 8010:8000 ${IMAGE_NAME}:${IMAGE_TAG}
                    # Damos unos segundos a que arranque uvicorn
                    sleep 8
                    # Consultamos el health check; -f hace fallar el stage si no responde 2xx
                    docker exec smoke_test python -c "import urllib.request,sys; r=urllib.request.urlopen('http://localhost:8000/health'); sys.exit(0 if r.status==200 else 1)"
                    echo "Health check OK"
                """
            }
            post {
                always {
                    // Paramos el contenedor de prueba pase lo que pase
                    sh 'docker stop smoke_test || true'
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
                    '''
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${IMAGE_NAME}:${GIT_SHA}"
                    sh "docker push ${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        success {
            echo "CD completado. Imagen publicada: ${IMAGE_NAME}:${IMAGE_TAG} (commit ${GIT_SHA})"
        }
        failure {
            echo "El pipeline de CD fallo. Revisar los logs del stage correspondiente."
        }
        always {
            sh 'docker logout || true'
            sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:${GIT_SHA} ${IMAGE_NAME}:latest || true"
        }
    }
}
