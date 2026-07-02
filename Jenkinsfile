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
                sh 'python3 --version'
            }
        }

        stage('Install Requirements') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Train Model') {
            steps {
                sh 'python3 train.py'
            }
        }

        stage('Pipeline Completed') {
            steps {
                echo 'Travel Intelligence Platform Pipeline Executed Successfully!'
            }
        }
    }
}