def sc
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
                sh 'pip3 install -v mysql-connector-python-rf==2.2.2'
                sh 'python3 create_table.py carmeldev kaltura XeIwD4STBaiUwOc'
            }
        }
        stage('connect to DB') {
            steps {
                echo 'test'
            }
        }
    }
}

