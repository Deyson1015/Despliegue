pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "urrego/backend_personas"
        FRONTEND_IMAGE = "urrego/frontend_personas"
        BACKEND_PORT = '5000'
        FRONTEND_PORT = '5173'

        // URL del webhook de Render
        RENDER_HOOK_BACKEND = "https://api.render.com/deploy/srv-d3tfrjili9vc73bbatg0?key=5VGOW2ELP0o"
        RENDER_HOOK_FRONTEND = "https://api.render.com/deploy/srv-d3tgb07diees73dhc2pg?key=vVmiLSQLLHs"
    }

    // Webhook para GitHub Push
    triggers {

        githubPush()

    }

    stages {

        stage('Checkout') {
            steps {
                echo ' Descargando código desde GitHub...'
                withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    git(
                        url: 'https://github.com/Deyson1015/Despliegue.git',
                        credentialsId: 'github-token',
                        branch: 'main'
                    )
                }
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
                echo '  Notificando despliegue de backend a Render...'
                bat """
                    curl -X POST %RENDER_HOOK_BACKEND%
                    echo " Despliegue de backend notificado a Render."
                """
                echo '  Notificando despliegue de frontend a Render...'
                bat """
                    curl -X POST %RENDER_HOOK_FRONTEND%
                    echo " Despliegue de frontend notificado a Render."
                """
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
