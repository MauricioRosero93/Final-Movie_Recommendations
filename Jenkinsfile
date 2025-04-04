pipeline {
    agent any
    
    environment {
        PYTHON = "C:\\Users\\Asus\\Final-Movie_Recommendations\\.venv\\Scripts\\python.exe"
    }
    
    stages {
        stage('Instalar Dependencias') {
            steps {
                bat "\"${env.PYTHON}\" -m pip install pytest numpy pandas scikit-surprise"
            }
        }
        
        stage('Ejecutar Pruebas') {
            steps {
                bat "\"${env.PYTHON}\" -m pytest tests/ --junitxml=test-results/results.xml"
            }
        }
        
        stage('Ejecutar Pipeline') {
            steps {
                bat "\"${env.PYTHON}\" pipeline/data_processing.py"
                bat "\"${env.PYTHON}\" pipeline/model_training.py"
                bat "\"${env.PYTHON}\" pipeline/model_evaluation.py"
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