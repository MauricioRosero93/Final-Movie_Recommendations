pipeline {
    agent any
    
    environment {
        // 1. Usa rutas absolutas para Python y dependencias
        PYTHON_PATH = "C:\\Users\\Asus\\Final-Movie_Recommendations\\.venv\\Scripts\\python.exe"
        PROJECT_DIR = "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Final-Movie_Recommendations"
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                // 2. Instalar dependencias necesarias
                bat """
                    call "%PYTHON_PATH%" -m pip install --upgrade pip
                    call "%PYTHON_PATH%" -m pip install pytest pytest-cov pytest-html
                    call "%PYTHON_PATH%" -m pip install -r requirements.txt
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                // 3. Ejecutar tests con cobertura (formato Windows)
                bat """
                    cd "%PROJECT_DIR%"
                    call "%PYTHON_PATH%" -m pytest tests/ --cov=. --cov-report=xml:coverage_report/coverage.xml --junitxml=test-reports/results.xml
                """
            }
        }
        
        stage('Execute Pipeline') {
            steps {
                // 4. Ejecutar pasos del pipeline
                bat """
                    cd "%PROJECT_DIR%"
                    call "%PYTHON_PATH%" pipeline/data_processing.py
                    call "%PYTHON_PATH%" pipeline/model_training.py
                    call "%PYTHON_PATH%" pipeline/model_evaluation.py
                """
            }
        }
    }
    
    post {
        always {
            // 5. Publicar resultados
            junit 'test-reports/results.xml'
            cobertura coberturaReportFile: 'coverage_report/coverage.xml'
            
            // 6. Limpieza opcional
            cleanWs()
        }
    }
}