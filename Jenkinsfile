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
                script {
                    env.BASE_PATH = "server/"
                    env.CREATE_TABLE_SCRIPT = "${env.BASE_PATH}"+'deployment/base/sql/01.kaltura_sphinx_ce_tables.sql'
                    env.PERMISSION_SCRIPT = "${env.BASE_PATH}"+'deployment/permissions/'
                }
            }
        }
        stage('clone kaltura server') {
            when { expression { return !fileExists (env.BASE_PATH) } }
            steps {
                 sh 'git clone https://github.com/kaltura/server.git'
            }
        }
        stage('connect to DB') {
            steps {
                sh "mysql -h${params.DB_URL} -u${params.DB_USER} -p${params.DB_PASSWORD}"
                echo "connect successfully :  mysql -h${params.DB_URL} -u${params.DB_USER} -p${params.DB_PASSWORD}"
            }
        }
        stage('create tables') {
            when { expression { return fileExists (env.CREATE_TABLE_SCRIPT) } }
            steps {
                echo "${env.CREATE_TABLE_SCRIPT}"
                sh "mysql -h${params.DB_URL} -u${params.DB_USER} -p${params.DB_PASSWORD} < ${env.CREATE_TABLE_SCRIPT}"
            }
        }
        stage('collect permissions file') {
            steps {
                script {
                        sh 'touch server/deployment/db.ini'
                        env.BASE_PERMISSION_SCRIPT = "${env.BASE_PATH}"+"alpha/scripts/utils/permissions/addPermissionsAndItems.php"
//                         env.DB_INI = "[datasources] \n default = propel \n propel.adapter = mysql propel.connection.classname = KalturaPDO propel.connection.phptype = mysql propel.connection.database = kaltura propel.connection.hostspec = "+"${params.DB_URL}"+" propel.connection.user = "+"${params.DB_USER} "+" propel.connection.password = "+"${params.DB_PASSWORD} "+" propel.connection.dsn = \"mysql:host= "+"${params.DB_URL}"+";port=3306;dbname=kaltura;\" propel.connection.options.kaltura.noTransaction = true"
                        env.DB_INI = "carmel "
//                         sh 'echo ${env.DB_INI} >> touch server/deployment/db.ini'
                        def data = """
                        [datasources]
                        default = propel
                        propel.adapter = mysql
                        propel.connection.classname = KalturaPDO
                        propel.connection.phptype = mysql
                        propel.connection.database = kaltura
                        propel.connection.hostspec = ${params.DB_URL}
                        propel.connection.user = ${params.DB_USER}
                        propel.connection.password = ${params.DB_PASSWORD}
                        propel.connection.dsn = \"mysql:host=${params.DB_URL};port=3306;dbname=kaltura;\"
                        propel.connection.options.kaltura.noTransaction = true"""
                        writeFile(file: 'server/deployment/db.ini', text: data)
                        sleep 30
//                         File file = new File("server/deployment/db.ini")
// //                         file.write("hello\n")
//                         file.append("[datasources] \n default = propel \n propel.adapter =")
//                         file.append("[datasources] \n default = ${params.DB_URL}")
// //                         println file.text
//                         sleep 20
// //                         sh 'echo test ${params.DB_URL} >> db.ini'
                        files = findFiles(glob: ' ${env.PERMISSION_SCRIPT}*.ini')
                        for (int i = 0; i < files.size(); i++) {
                                def filename = files[i]
                                echo "${filename}\n"
//                                 sh 'php ${env.CREATE_TABLE_SCRIPT} ${filename}'
                              }
                      }
                sleep 20
            }
        }
    }
}

