#!/bin/bash

DB_URL=$1
DB_USER=$2
DB_PASSWORD=$3
SERVICE_URL="http://$4"
HOST=$4
WEB_DIR="/opt/kaltura/web"


SOURCE_FILE='/server/configuration/db.template.ini'
DEST_FILE=`echo $SOURCE_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
sed -e "s#@DB1_HOST@#$DB_URL/#g" -e "s#@DB1_USER@#$DB_USER/#g" -e "s#@DB1_PASS@#$DB_PASSWORD/#g" -e "s#@DB1_PORT@#3306/#g" $DEST_FILE

SOURCE_FILE='/server/configuration/dc_config.template.ini'
DEST_FILE=`echo $SOURCE_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
sed -e "s#@SERVICE_URL@#$SERVICE_URL/#g" -e "s#@WEB_DIR@#$WEB_DIR/#g" $DEST_FILE

SOURCE_FILE='/server/configuration/local.template.ini'
DEST_FILE=`echo $SOURCE_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
sed -e "s#@WWW_HOST@#$HOST/#g" -e "s#@WEB_DIR@#$WEB_DIR/#g" -e "s#@SERVICE_URL@#$SERVICE_URL/#g" -e "s#@DWH_HOST@#$DB_URL/#g" -e "s#@DWH_USER@#$DB_USER/#g" -e "s#@DWH_PASS@#$DB_PASSWORD/#g" -e "s#@DWH_PORT@#3306/#g" -e "s#@DWH_DATABASE_NAME@#kaltura/#g" $DEST_FILE
