#!/bin/bash

#INIT_CONTENT='/init_content'
INIT_CONTENT=$1
SERVICE_URL="http://$2"
DB_CONN="mysql -N -h$5 -u$6 -p$7 kaltura"
ADMIN_CONSOLE_ADMIN_MAIL=$3
ADMIN_CONSOLE_PASSWORD=$4
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

#add user -2
USER_SET_1=`echo "select id from kuser where partner_id='-2'"|$DB_CONN`
echo "user -2 $USER_SET_1"

if [ -z "$USER_SET_1" ]
then
  echo 'create user -2'
  php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/01.UserRole.-2.xml
fi

#add user 99
USER_SET_2=`echo "select id from kuser where partner_id='99'"|$DB_CONN`
echo "user 99 $USER_SET_2"
if [ -z "$USER_SET_2" ]
then
  echo 'create user 99'
  php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/01.UserRole.99.xml
fi


#echo "start working on accessControl "
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/01.accessControl.xml
#
#echo "start working on conversionProfile 99"
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/01.conversionProfile.99.xml
#
#echo "start working on conversionProfile -4"
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/01.conversionProfile.-4.xml
#
#echo "start working on 03.EventNotificationTemplate.0.xml "
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/03.EventNotificationTemplate.0.xml
#
#echo "start working on 02.playlist.99.xml "
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/02.playlist.99.xml
#
#
#echo "start working on 05.responseProfiles.0.xml"
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/05.responseProfiles.0.xml
#
#echo "start working on entry.99 "
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/02.entry.99.xml
#
##
#echo "start working on entry. -4 "
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/02.entry.-4.xml
#
#echo "start working on 04.dropFolder.-4.xml"
#php server/tests/standAloneClient/exec.php server/deployment/base/scripts/init_content/04.dropFolder.-4.xml



#for file in `find .$INIT_CONTENT/ -name "*.xml" -not -name "*.template*" -not -name "*UserRole*" `;do
#        echo "start working on $file"
#        php server/tests/standAloneClient/exec.php $file
#done





