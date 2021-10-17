#!/bin/bash

DB_URL=$1
DB_USER=$2
DB_PASSWORD=$3
SERVICE_URL="http://$4"
HOST=$4
WEB_DIR="/opt/kaltura/web"


SOURCE_FILE='/server/configuration/db.template.ini'
DEST_FILE=`echo $SOURCE_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
sed -i "s#@DB1_HOST@#$DB_URL/#g" "s#@DB1_USER@#$DB_USER/#g" "s#@DB1_PASS@#$DB_PASSWORD/#g" "s#@DB1_PORT@#3306/#g" $DEST_FILE

SOURCE_FILE='/server/configuration/dc_config.template.ini'
DEST_FILE=`echo $SOURCE_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
sed -i "s#@SERVICE_URL@#$SERVICE_URL/#g" "s#@WEB_DIR@#$WEB_DIR/#g" $DEST_FILE

SOURCE_FILE='/server/configuration/local.template.ini'
DEST_FILE=`echo $SOURCE_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
sed -i "s#@WWW_HOST@#$HOST/#g" "s#@WEB_DIR@#$WEB_DIR/#g" "s#@SERVICE_URL@#$SERVICE_URL/#g" "s#@DWH_HOST@#$DB_URL/#g" "s#@DWH_USER@#$DB_USER/#g" "s#@DWH_PASS@#$DB_PASSWORD/#g" "s#@DWH_PORT@#3306/#g" "s#@DWH_DATABASE_NAME@#kaltura/#g" $DEST_FILE
