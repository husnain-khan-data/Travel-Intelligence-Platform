pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking project...'
            }
        }

        stage('Python Version') {
            steps {
                bat 'python --version'
            }
        }

        stage('Install Requirements') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Train Model') {
            steps {
                bat 'python train.py'
            }
        }

        stage('Pipeline Completed') {
            steps {
                echo 'Travel Intelligence Platform Pipeline Executed Successfully!'
            }
        }
    }
}