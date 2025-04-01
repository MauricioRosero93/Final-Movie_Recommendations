pipeline {
    agent any
    
    environment {
        PYTHON = 'python'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat "${PYTHON} -m pip install -r requirements.txt"
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                bat "${PYTHON} -m unittest discover tests/"
            }
        }
        
        stage('Train Models') {
            steps {
                bat "${PYTHON} train_models.py"
            }
        }
        
        stage('Evaluate Models') {
            steps {
                bat "${PYTHON} evaluate_models.py"
            }
        }
        
        stage('Run API Tests') {
            steps {
                script {
                    try {
                        // Iniciar la API en segundo plano
                        bat "start ${PYTHON} app.py"
                        
                        // Esperar que la API esté lista
                        sleep(time: 10, unit: 'SECONDS')
                        
                        // Ejecutar tests
                        bat "${PYTHON} -m unittest tests/test_api.py"
                    } finally {
                        // Detener la API
                        bat "taskkill /IM python.exe /F"
                    }
                }
            }
        }
    }
    
    post {
        always {
            junit '**/test-reports/*.xml'
        }
    }
}