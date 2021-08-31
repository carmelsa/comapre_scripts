pipeline {
    agent { docker { image 'python:3.5.1' } }
    parameters {
        string(name: 'HOST_URL',defaultValue: '', description: 'DB host url')
        string(name: 'HOST_URL_1',defaultValue: '', description: 'DB host url_1')

    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                echo "host url is ${params.HOST_URL}"
                sh 'pip3 install mysql-connector-python'
            }
        }
        stage('connect to DB') {
            steps {
                script {
                sc = load "deployment/base/sql/01.kaltura_ce_tables.sql"
                }
                echo 'test ${sc}'

                echo 'test'
            }
        }
    }
}

