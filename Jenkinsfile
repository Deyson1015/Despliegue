pipeline {
    agent any
    
    environment {
        BACKEND_IMAGE = 'gestion-personas-backend'
        FRONTEND_IMAGE = 'gestion-personas-frontend'
        DB_IMAGE = 'mysql:8.0'
        BACKEND_PORT = '5000'
        FRONTEND_PORT = '5173'
        DB_PORT = '3307'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo ' Descargando código...'
                checkout scm
            }
        }
        
        stage('Detener Contenedores') {
            steps {
                echo ' Deteniendo contenedores anteriores...'
                bat 'docker-compose down || exit 0'
            }
        }
        
        stage('Construir Imágenes') {
            steps {
                echo " Construyendo imágenes: ${BACKEND_IMAGE}, ${FRONTEND_IMAGE}, ${DB_IMAGE}"
                bat 'docker-compose build'
            }
        }
        
        stage('Iniciar Aplicación') {
            steps {
                echo " Iniciando contenedores en puertos: Backend:${BACKEND_PORT}, Frontend:${FRONTEND_PORT}, DB:${DB_PORT}"
                bat 'docker-compose up -d'
            }
        }
        
        stage('Verificar Estado') {
            steps {
                echo ' Verificando contenedores...'
                bat 'docker ps'
                echo " Backend: http://localhost:${BACKEND_PORT}"
                echo " Frontend: http://localhost:${FRONTEND_PORT}"
                echo " MySQL: localhost:${DB_PORT}"
            }
        }
    }
    
    post {
        success {
            echo ' ¡Despliegue exitoso!'
        }
        
        failure {
            echo ' El despliegue falló'
            bat 'docker-compose logs'
        }
    }
}
