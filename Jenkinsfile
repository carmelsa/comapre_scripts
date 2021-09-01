pipeline {
    agent { docker { image 'ubuntu:20.04' } }
    parameters {
        string(name: 'DB_URL',defaultValue: '10.100.102.59', description: 'DB host url')
        string(name: 'DB_USER',defaultValue: 'root', description: 'DB user')
        password(name: 'DB_PASSWORD',defaultValue: 'root', description: 'DB password')

    }
    stages {
        stage('build') {
            steps {
                sh 'apt-get update && apt-get install -y python3 python3-pip git'
//                 sh 'apt-get install -y mysql-server'
                sh 'python3 --version'
     //           echo "host url is ${params.DB_URL}"
//                 sh 'pip3 install mysql-connector-python'
                sh 'apt-get install -y mysql-client'
                sh 'git clone https://github.com/kaltura/server.git'
                script {
                    env.BASE_PATH = "server/"
                    env.CREATE_TABLE_SCRIPT = "${env.BASE_PATH}"+'server/deployment/base/sql/01.kaltura_sphinx_ce_tables.sql'
                }
                echo "${env.CREATE_TABLE_SCRIPT}"
            }
        }
        stage('connect to DB') {
            when { expression { return fileExists (create_table_script) } }
            steps {
                echo "mysql -h${params.DB_URL} -u${params.DB_USER} -p${params.DB_PASSWORD}"
                sh "mysql -h${params.DB_URL} -u${params.DB_USER} -p${params.DB_PASSWORD} < ${env.CREATE_TABLE_SCRIPT}"
            }
        }
    }
}

