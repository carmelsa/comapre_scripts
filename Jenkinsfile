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

def local_data = """date_default_timezone = Israel
query_cache_enabled = false
query_cache_invalidate_on_change = false
sphinx_query_cache_enabled = false
sphinx_query_cache_invalidate_on_change = false
[reports_db_config]
host = ${params.DB_URL}
user = ${params.DB_USER}
port = 3306
password = ${params.DB_PASSWORD}
db_name = kaltura
"""



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
                sh 'DEBIAN_FRONTEND=noninteractive apt-get install -y php7.4'
                sh 'apt-get install -y mysql-client '
                sleep 20
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
//         stage('clone kaltura server-saas-clients') {
// //             when { expression { return !fileExists (env.BASE_PATH) } }
//             steps {
//                  sh 'git clone https://github.com/kaltura/server-saas-clients.git'
//             }
//         }
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
                        sh 'touch server/configurations/db.ini'
//                         env.BASE_PERMISSION_SCRIPT = "${env.BASE_PATH}"+"alpha/scripts/utils/permissions/addPermissionsAndItems.php"
                        writeFile(file: 'server/configurations/db.ini', text: data)
                        sh 'touch server/configurations/local.ini'
                        sh 'mkdir -p server/cache/scripts'
                        writeFile(file: 'server/configurations/local.ini', text: local_data)
                        files = findFiles(glob: 'server/deployment/permissions/*.ini')
                        echo "file path is ${env.PERMISSION_SCRIPT}"
                        echo "file size is" + files.size()
                        sh 'pwd'
                        sleep 20
                        dir('server')
                        {
                            sh 'pwd'
                            sh 'php alpha/scripts/utils/permissions/addPermissionsAndItems.php deployment/permissions/object.KalturaAdCuePoint.ini'
                        }
                        for (int i = 0; i < files.size(); i++) {
                                def filename = files[i]
                                echo "${filename}\n"
//                                 echo "/alpha/scripts/utils/permissions/addPermissionsAndItems.php ${filename}"
//                                 sh 'php server/alpha/scripts/utils/permissions/addPermissionsAndItems.php ${filename}'
                                //                                sh 'php ${env.CREATE_TABLE_SCRIPT} ${filename}'

                                echo 'done'
                              }
                      }
            }
        }
    }
}

