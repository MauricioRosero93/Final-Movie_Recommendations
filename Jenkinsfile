pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                bat 'python -m pytest tests/ --cov=./ --cov-report=xml:coverage_report/coverage.xml'
            }
        }
        
        stage('Pipeline Execution') {
            steps {
                bat 'python pipeline/data_processing.py'
                bat 'python pipeline/model_training.py'
                bat 'python pipeline/model_evaluation.py'
            }
        }
    }
    
    post {
        always {
            junit '**/test-reports/*.xml'
            cobertura coberturaReportFile: 'coverage_report/coverage.xml'
        }
    }
}