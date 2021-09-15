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
propel.connection.options.kaltura.noTransaction = true
"""

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
encryption_iv = RAoykFop9b5dJ7ZD
"""

dc_config = """current = 0
[list]
0.id = 0
0.name = DC_0
0.url = http://carmeldev
0.secret = @DC0_SECRET@
0.root = /opt/kaltura/web/

; object types and sub types that shouldn't be synced
; key value structrue is: name = {object type}[:{object sub type}]
[sync_exclude_types]
FILE_SYNC_ENTRY_SUB_TYPE_CONVERSION_LOG = 1:9
FILE_SYNC_ENTRY_SUB_TYPE_LIVE_PRIMARY = 1:10
FILE_SYNC_ENTRY_SUB_TYPE_LIVE_SECONDARY = 1:11
BATCHJOB = 3
FILE_SYNC_ASSET_SUB_TYPE_CONVERT_LOG = 4:2
FILE_SYNC_ASSET_SUB_TYPE_LIVE_PRIMARY = 4:5
FILE_SYNC_ASSET_SUB_TYPE_LIVE_SECONDARY = 4:6
ENTRY_DISTRIBUTION = contentDistribution.EntryDistribution """



pipeline {
    agent { docker { image 'ubuntu:20.04' } }
    parameters {
        string(name: 'DB_URL',defaultValue: '10.100.102.59', description: 'DB host url')
        string(name: 'DB_USER',defaultValue: 'root', description: 'DB user')
        password(name: 'DB_PASSWORD',defaultValue: 'root', description: 'DB password')
        booleanParam(name: 'create_tables', defaultValue: false, description: 'mark true if you want to run create tables script')
        booleanParam(name: 'set_permissions', defaultValue: false, description: 'mark true if you want to set permissions')
        booleanParam(name: 'set_init_file', defaultValue: true, description: 'mark true if you want to set init data')

        }
    stages {
        stage('build') {
            steps {
                sh 'DEBIAN_FRONTEND=noninteractive apt-get install -y php7.4 php7.4-mysql'
                sh 'apt-get update && apt-get install -y python3 python3-pip git unzip mysql-client'
//                 sh 'apt-get install -y mysql-server'
                sh 'python3 --version'
     //           echo "host url is ${params.DB_URL}"
//                 sh 'pip3 install mysql-connector-python'
                sh 'useradd kaltura'
                script {
                    env.BASE_PATH = "server/"
                    env.CREATE_TABLE_SCRIPT = "${env.BASE_PATH}"+'deployment/base/sql/01.kaltura_ce_tables.sql'
                    sh 'touch server/configurations/db.ini'
                    writeFile(file: 'server/configurations/db.ini', text: data)
                    sh 'touch server/configurations/local.ini'
                    sh 'mkdir -p server/cache/scripts'
                    writeFile(file: 'server/configurations/local.ini', text: local_data)
                    if ( fileExists ("server-saas-clients-Quasar-17.10.0") == false)
                    {
                        sh 'unzip server-saas-clients-Quasar-17.10.0.zip'
                    }
                    writeFile(file: 'server/configurations/dc_config.ini', text: dc_config)
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
         when {
          allOf {
            expression { return fileExists (env.CREATE_TABLE_SCRIPT)}
            expression { return params.create_tables }
            }
          }
            steps {
                echo "${env.CREATE_TABLE_SCRIPT}"
                sh "mysql -h${params.DB_URL} -u${params.DB_USER} -p${params.DB_PASSWORD} < ${env.CREATE_TABLE_SCRIPT}"
            }
        }
        stage('permissions file') {
            when {
                expression { return params.set_permissions }
            }
            steps {
                script {
                        dir('server')
                        {
                            files = findFiles(glob: 'deployment/permissions/*.ini')
                            echo "file size is " + files.size()
                            sh 'pwd'
                            for (int i = 0; i < files.size(); i++) {
                                def filename = files[i]
                                sh "php alpha/scripts/utils/permissions/addPermissionsAndItems.php $filename"
                              }
                            plugin_files = findFiles(glob: 'plugins/**/permissions.ini')
                            echo "plugin_files size is " + plugin_files.size()
                            for (int i = 0; i < plugin_files.size(); i++) {
                                def filename = plugin_files[i]
                                sh "php alpha/scripts/utils/permissions/addPermissionsAndItems.php $filename"
                              }
                        }
                }

            }
        }
         stage('init data') {
             when {
               allOf {
               expression { return params.set_init_file }
               expression { return fileExists ("server-saas-clients-Quasar-17.10.0")}
                }
            }
            steps {
                script {
                        dir('server')
                        {
                            sleep 20
                            files = findFiles(glob: 'deployment/base/scripts/init_data/*.ini')
                            echo "file init data size is " + files.size()
                            sh 'php deployment/base/scripts/insertDefaults.php deployment/base/scripts/init_data'
                            for (int i = 0; i < files.size(); i++) {
                                def filename = files[i]
                            //    sh "php deployment/base/scripts/insertDefaults.php $filename"

                              }
                        }
                }

            }
        }
    }
}

