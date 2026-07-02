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

        stage('Pipeline Completed') {
            steps {
                echo 'Travel Intelligence Platform Pipeline Executed Successfully!'
            }
        }
    }
}