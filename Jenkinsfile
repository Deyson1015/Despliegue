pipeline {
    agent any
    
    environment {
        // Nombres de las imágenes en Docker Hub
        BACKEND_IMAGE = "urrego/backend_personas"
        FRONTEND_IMAGE = "urrego/frontend_personas"

        // Variables locales
        BACKEND_PORT = '5000'
        FRONTEND_PORT = '5173'
    }
    
    stages {

        stage('Checkout') {
            steps {
                echo ' Descargando código desde GitHub...'
                checkout scm
            }
        }

        stage('Construir Imágenes Docker') {
            steps {
                echo " Construyendo imágenes Docker..."
                dir("${env.WORKSPACE}") {
                    bat '''
                        set DOCKER_BUILDKIT=0
                        set COMPOSE_DOCKER_CLI_BUILD=0
                        docker-compose build --no-cache
                    '''
                }
            }
        }

        stage('Login en Docker Hub') {
            steps {
                echo ' Iniciando sesión en Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    '''
                }
            }
        }

        stage('Etiquetar Imágenes') {
            steps {
                echo ' Etiquetando imágenes...'
                bat """
                    docker tag despliegue-backend:latest ${BACKEND_IMAGE}:latest
                    docker tag despliegue-frontend:latest ${FRONTEND_IMAGE}:latest
                """
            }
        }

        stage('Publicar en Docker Hub') {
            steps {
                echo ' Subiendo imágenes a Docker Hub...'
                bat """
                    docker push ${BACKEND_IMAGE}:latest
                    docker push ${FRONTEND_IMAGE}:latest
                """
            }
        }

        stage('Limpiar Imágenes Locales') {
            steps {
                echo ' Limpiando imágenes locales...'
                bat 'docker image prune -f'
            }
        }

        stage('Notificar a Render') {
            steps {
                echo ' Imágenes publicadas en Docker Hub'
                echo "   Backend: ${BACKEND_IMAGE}:latest"
                echo "   Frontend: ${FRONTEND_IMAGE}:latest"
            }
        }
    }

    post {
        success {
            echo ' Pipeline completado exitosamente. Imágenes listas en Docker Hub.'
        }

        failure {
            echo 'El pipeline falló, mostrando logs...'
            dir("${env.WORKSPACE}") {
                bat 'docker-compose logs || exit 0'
            }
        }

        always {
            echo ' Cerrando sesión de Docker Hub'
            bat 'docker logout || exit 0'
        }
    }
}
