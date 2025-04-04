pipeline {
    agent any
    
    stages {
        stage('Instalar Dependencias') {
            steps {
                bat 'python -m pip install pytest numpy pandas scikit-surprise'
            }
        }
        
        stage('Ejecutar Pruebas') {
            steps {
                bat 'python -m pytest tests/ --junitxml=test-results/results.xml'
            }
            
            post {
                always {
                    archiveArtifacts artifacts: 'test-results/results.xml'
                }
            }
        }
        
        stage('Ejecutar Pipeline') {
            steps {
                bat 'python pipeline/data_processing.py'
                bat 'python pipeline/model_training.py'
                bat 'python pipeline/model_evaluation.py'
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