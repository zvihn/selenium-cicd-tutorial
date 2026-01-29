// Jenkinsfile - Jenkins Pipeline Configuration
// This is the Jenkins equivalent of .github/workflows/selenium-tests.yml

pipeline {
    // Define where the pipeline runs
    agent any
    
    // Environment variables (like 'env:' in GitHub Actions)
    environment {
        PYTHON_VERSION = '3.11'
        FLASK_ENV = 'production'
        HEADLESS = 'true'
        APP_URL = 'http://127.0.0.1:5000'
    }
    
    // Pipeline stages (like 'steps:' in GitHub Actions)
    stages {
        
        // Stage 1: Checkout Code
        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                checkout scm
            }
        }
        
        // Stage 2: Setup Python Environment
        stage('Setup Python') {
            steps {
                echo '🐍 Setting up Python environment...'
                sh '''
                    # Create virtual environment
                    python3 -m venv venv
                    
                    # Activate and install dependencies
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        // Stage 3: Install Chrome (if not already installed)
        stage('Setup Chrome') {
            steps {
                echo '🌐 Verifying Chrome installation...'
                sh '''
                    # Check if Chrome is installed
                    if ! command -v google-chrome &> /dev/null && \
                       ! command -v /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome &> /dev/null
                    then
                        echo "Chrome not found, please install Chrome"
                        exit 1
                    fi
                    
                    # Show Chrome version
                    if command -v google-chrome &> /dev/null; then
                        google-chrome --version
                    else
                        /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version
                    fi
                '''
            }
        }
        
        // Stage 4: Start Flask Application
        stage('Start Application') {
            steps {
                echo '🚀 Starting Flask application...'
                sh '''
                    # Activate virtual environment
                    . venv/bin/activate
                    
                    # Start Flask in background
                    cd app
                    python app.py &
                    echo $! > flask.pid
                    cd ..
                    
                    # Wait for app to start
                    sleep 5
                    
                    # Verify app is running
                    curl -f http://127.0.0.1:5000 || (echo "App failed to start" && exit 1)
                '''
            }
        }
        
        // Stage 5: Run Selenium Tests
        stage('Run Tests') {
            steps {
                echo '🧪 Running Selenium tests...'
                sh '''
                    # Activate virtual environment
                    . venv/bin/activate
                    
                    # Run tests
                    python tests/test_selenium.py
                '''
            }
        }
    }
    
    // Post actions (run after all stages)
    post {
        // Always run (cleanup)
        always {
            echo '🧹 Cleaning up...'
            sh '''
                # Stop Flask if running
                if [ -f app/flask.pid ]; then
                    kill $(cat app/flask.pid) || true
                    rm app/flask.pid
                fi
                
                # Deactivate virtual environment
                deactivate || true
            '''
        }
        
        // On success
        success {
            echo '✅ All tests passed!'
        }
        
        // On failure
        failure {
            echo '❌ Tests failed!'
            // You can add notifications here
        }
        
        // On unstable (some tests failed)
        unstable {
            echo '⚠️ Some tests failed but build continued'
        }
    }
}