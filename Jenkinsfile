pipeline {
    agent any
    
    environment {
        PYTHON = "C:\\Users\\Asus\\Final-Movie_Recommendations\\.venv\\Scripts\\python.exe"
    }
    
    stages {
        stage('Instalar Dependencias') {
            steps {
                bat "\"${env.PYTHON}\" -m pip install -e ."
            }
        }
        
        stage('Ejecutar Pruebas') {
            steps {
                bat "\"${env.PYTHON}\" -m pytest tests/ --junitxml=test-results/results.xml"
            }
        }
        
        stage('Ejecutar Pipeline') {
            steps {
                // Ejecutar como módulos Python
                bat "\"${env.PYTHON}\" -m pipeline.data_processing"
                bat "\"${env.PYTHON}\" -m pipeline.model_training"
                bat "\"${env.PYTHON}\" -m pipeline.model_evaluation"
            }
        }
    }
    
    post {
        always {
            junit 'test-results/results.xml'
            cleanWs()
        }
    }
}