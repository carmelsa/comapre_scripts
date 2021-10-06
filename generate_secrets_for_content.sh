#!/bin/bash

#INIT_CONTENT='/init_content'
INIT_CONTENT=$1
SERVICE_URL=$2
DB_CONN=$3
ADMIN_CONSOLE_ADMIN_MAIL=$4
ADMIN_CONSOLE_PASSWORD=$5
WEB_DIR="/opt/kaltura/web"
echo "connecting to : $DB_CONN"
TEMPLATE_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=99"|$DB_CONN`
ADMIN_CONSOLE_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=-2"|$DB_CONN`
MONITOR_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=-4"|$DB_CONN`

UI_CONF_DIR=$INIT_DATA'/ui_conf'

# fill init content templates
for TMPL in `find .$INIT_CONTENT/ -name "*template*" `;do
        echo $TMPL
        DEST_FILE=`echo $TMPL | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
        cp  $TMPL $DEST_FILE
        sed -e "s#@WEB_DIR@#$BASE_DIR/web#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$TEMPLATE_PARTNER_ADMIN_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$ADMIN_CONSOLE_PARTNER_ADMIN_SECRET#g" -e "s#@MONITOR_PARTNER_ADMIN_SECRET@#$MONITOR_PARTNER_ADMIN_SECRET#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g"   -e "s/@ADMIN_CONSOLE_PASSWORD@/$ADMIN_CONSOLE_PASSWORD/g"  -i $DEST_FILE
done






