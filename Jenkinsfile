pipeline {
    agent { docker { image 'python:3.5.1' } }
    parameters {
        string(name: 'HOST_URL',defaultValue: '', description: 'DB host url')
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                echo "host url is ${params.HOST_URL}"
                sh 'pip install --upgrade pip'
                sh 'pip install mysql-connector-python'
            }
        }
        stage('connect to DB') {
            steps {
                echo 'test'
            }
        }
    }
}

