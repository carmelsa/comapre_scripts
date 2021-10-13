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
encryption_iv = "RAoykFop9b5dJ7ZD"
[reports_db_config]
host = ${params.DB_URL}
user = ${params.DB_USER}
port = 3306
password = ${params.DB_PASSWORD}
db_name = kaltura

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
        booleanParam(name: 'set_init_file', defaultValue: false, description: 'mark true if you want to set init data')
        string(name: 'LIVE_PACKAGER_HOST',defaultValue: '10.100.102.53', description: 'if the port is different from 80, please add :port to the host')
        string(name: 'VOD_PACKAGER_HOST',defaultValue: '10.100.102.53', description: 'if the port is different from 80, please add :port to the host')
        string(name: 'WWW_HOST',defaultValue: '10.100.102.53', description: 'if the port is different from 80, please add :port to the host')
        booleanParam(name: 'set_user', defaultValue: true, description: 'mark true if you want to set the init content')
        string(name: 'USER_EMAIL',defaultValue: 'admin@kaltura.com', description: 'add user email')
        password(name: 'USER_PASSWORD',defaultValue: 'root', description: 'user password')
        }
    stages {
        stage('build') {
            steps {
                sh 'apt-get update && apt-get install -y python3 python3-pip git unzip vim locate mysql-client'
                sh 'DEBIAN_FRONTEND=noninteractive apt-get install -y php7.4 php7.4-mysql php7.4-curl php-mbstring php-dom'
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
                    else
                    {
                        if ( fileExists ("server/tests/lib") == false)
                        {
                            sh 'cp -r server-saas-clients-Quasar-17.10.0/tests/lib server/tests/'
                        }
                    }
                    if ( fileExists ("server-saas-config-Quasar-17.11.0") == false)
                    {
                        sh 'unzip server-saas-config-Quasar-17.11.0.zip'
                        sh 'cp server-saas-config-Quasar-17.11.0/configurations/plugins.ini.admin server/configurations'
                        sh 'cp  server-saas-config-Quasar-17.11.0/configurations/plugins.ini.base server/configurations'
                    }
                    writeFile(file: 'server/configurations/dc_config.ini', text: dc_config)
                    sh 'find server/cache/ -type f -delete'
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
                timeout(time: 1, unit: 'MINUTES')
                {
                   sh "mysql -h${params.DB_URL} -u${params.DB_USER} -p${params.DB_PASSWORD}"
                }
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
        stage('prepare template') {
             when {
               allOf {
               expression { return fileExists ("server-saas-config-Quasar-17.11.0")}
               expression { return params.set_init_file }
                }
            }
            steps {
            sh 'chmod +x generate_secrets_for_ini.sh'
            sh "./generate_secrets_for_ini.sh /server/deployment/base/scripts/init_data ${params.LIVE_PACKAGER_HOST} ${params.VOD_PACKAGER_HOST} ${params.WWW_HOST}"
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
                                sh "php alpha/scripts/utils/permissions/addPermissionsAndItems.php $filename >> addPermissionsAndItemsLog.txt"
                              }
                            plugin_files = findFiles(glob: 'plugins/**/permissions.ini')
                            echo "plugin_files size is " + plugin_files.size()
                            sleep 20
                            for (int i = 0; i < plugin_files.size(); i++) {
                                def filename = plugin_files[i]
                                sh "php alpha/scripts/utils/permissions/addPermissionsAndItems.php $filename >> addPermissionsAndItemsLog.txt"
                              }
                        }
                }

            }
        }
         stage('init data') {
             when {
               allOf {
               expression { return params.set_init_file }
               expression { return fileExists ("server-saas-config-Quasar-17.11.0")}
                }
            }
            steps {
                script {
                        dir('server')
                        {
                            files = findFiles(glob: 'deployment/base/scripts/init_data/*.ini',excludes: 'deployment/base/scripts/init_data/*template.ini')
                            echo "file init data size is " + files.size()
                            echo "installPlugins"
                            sh 'php deployment/base/scripts/installPlugins.php'
                            echo "insertDefaults"
                            init_files = findFiles(glob: 'deployment/base/scripts/init_data/*', excludes: 'deployment/base/scripts/init_data/*DeliveryProfile*,deployment/base/scripts/init_data/*template.ini')
                            sh 'rm -r deployment/base/scripts/init_data_Ready; mkdir deployment/base/scripts/init_data_Ready'
                            echo "file size is " + init_files.size()
                            for (int i = 0; i < init_files.size(); i++) {
                                def filename = init_files[i]
                                sh "cp -pn $filename deployment/base/scripts/init_data_Ready"
                            }
                            sh 'php deployment/base/scripts/insertDefaults.php deployment/base/scripts/init_data_Ready'
                        }
                }

            }
        }
        stage('add user') {
             when {
               allOf {
               expression { return params.set_user }
               expression { return fileExists ("server-saas-config-Quasar-17.11.0")}
               expression { return fileExists ("server/tests/standAloneClient/exec.php")}
               expression { return fileExists ("server/deployment/base/scripts/init_content/01.UserRole.-2.template.xml")}
                }
            }
            steps {
                script {
                        echo "add user admin"
                        sh 'chmod +x generate_secrets_for_content.sh'
                        sh "./generate_secrets_for_content.sh /server/deployment/base/scripts/init_content  ${params.WWW_HOST} ${params.USER_EMAIL} ${params.USER_PASSWORD} ${params.DB_URL} ${params.DB_USER} ${params.DB_PASSWORD}"
                   //     sleep 20
                        //echo "start working on entry.99"
                        //sh 'php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/02.entry.99.xml'

                        //dir('server')
             //           {
                        //    files = findFiles(glob: 'deployment/base/scripts/init_content/*.xml',excludes: 'deployment/base/scripts/init_content/*template*')
                       //     echo "file init data size is " + files.size()
                       //     sleep 20
                         //   sh 'php tests/standAloneClient/exec.php deployment/base/scripts/init_content/01.UserRole.-2.xml'
                          //  sh 'php tests/standAloneClient/exec.php deployment/base/scripts/init_content/01.UserRole.99.xml'
                      //  }
                }

            }
        }
    }
}

