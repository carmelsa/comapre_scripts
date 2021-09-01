def sc
pipeline {
    agent { docker { image 'ubuntu:20.04' } }
    parameters {
        string(name: 'HOST_URL',defaultValue: '', description: 'DB host url')
        string(name: 'HOST_URL_1',defaultValue: '', description: 'DB host url_1')

    }
    stages {
        stage('build') {
            steps {
                sh 'apt-get update && apt-get install -y python3 python3-pip'
                sh 'python3 --version'
                echo "host url is ${params.HOST_URL}"
                sh 'pip3 install mysql-connector-python'
                sleep 30
                sh 'python3 create_table.py 192.168.56.101 kaltura XeIwD4STBaiUwOc'
            }
        }
        stage('connect to DB') {
            steps {
                echo 'test'
            }
        }
    }
}

