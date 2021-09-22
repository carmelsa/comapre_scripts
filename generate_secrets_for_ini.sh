#!/bin/bash

gen_partner_secret()
{
	PATTERN="A-Za-z0-9_~@#$%^*()_+-="
	SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@#$%^*()_+-=" | head -c100`
	HASHED_SECRET=`echo $SECRET|md5sum`
	SECRET=`echo $HASHED_SECRET|awk -F " " '{print $1}'`
	echo $SECRET
}

# gen secrets
ADMIN_SECRET=`gen_partner_secret`

ADMIN_CONSOLE_PARTNER_SECRET=`gen_partner_secret`

MONITOR_PARTNER_ADMIN_SECRET=`gen_partner_secret`

MONITOR_PARTNER_SECRET=`gen_partner_secret`

PARTNER_MONITORING_PROXY_ADMIN_SECRET=`gen_partner_secret`

PARTNER_MONITORING_PROXY_SECRET=`gen_partner_secret`

PARTNER_KMC_SSO_ADMIN_SECRET=`gen_partner_secret`

PARTNER_KMC_SSO_SECRET=`gen_partner_secret`

PARTNER_ZERO_ADMIN_SECRET=`gen_partner_secret`

PARTNER_ZERO_SECRET=`gen_partner_secret`

BATCH_PARTNER_ADMIN_SECRET=`gen_partner_secret`

BATCH_PARTNER_SECRET=`gen_partner_secret`

MEDIA_PARTNER_ADMIN_SECRET=`gen_partner_secret`

MEDIA_PARTNER_SECRET=`gen_partner_secret`

TEMPLATE_PARTNER_ADMIN_SECRET=`gen_partner_secret`
TEMPLATE_PARTNER_ADMIN_PASSWORD="0+`< /dev/urandom tr -dc "A-Za-z0-9_=@%$" | head -c8`=*1"

TEMPLATE_PARTNER_SECRET=`gen_partner_secret`

HOSTED_PAGES_PARTNER_ADMIN_SECRET=`gen_partner_secret`

HOSTED_PAGES_PARTNER_SECRET=`gen_partner_secret`

PLAY_PARTNER_ADMIN_SECRET=`gen_partner_secret`

PLAY_PARTNER_SECRET=`gen_partner_secret`

REACH_INTERNAL_PARTNER_ADMIN_SECRET=`gen_partner_secret`

REACH_INTERNAL_PARTNER_SECRET=`gen_partner_secret`

CNC_PARTNER_ADMIN_SECRET=`gen_partner_secret`

CNC_PARTNER_SECRET=`gen_partner_secret`

TEMPLATE_PARTNER_ADMIN_SECRET=`gen_partner_secret`

TEMPLATE_PARTNER_SECRET=`gen_partner_secret`

BASE_DIR_WEB="/opt/kaltura/web"

BASE_DIR_LOG="var/log"

#INIT_DATA='/init_data'
INIT_DATA=$1


# SQL statement files tokens:
for TMPL in `find .$INIT_DATA/ -name "*template*" -not -name "*DeliveryProfile*"`;do
        echo $TMPL
        DEST_FILE=`echo $TMPL | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
        sed -e "s/@TEMPLATE_PARTNER_ADMIN_SECRET@/$ADMIN_SECRET/g" -e "s#@STORAGE_BASE_DIR@#$BASE_DIR_WEB#g" -e "s#@LOG_DIR@#$BASE_DIR/log#g" -e "s#@WEB_DIR@#$BASE_DIR_WEB#g" -e "s/@TEMPLATE_PARTNER_SECRET@/$TEMPLATE_PARTNER_SECRET/g" -e "s/@TEMPLATE_PARTNER_ADMIN_SECRET@/$TEMPLATE_PARTNER_ADMIN_SECRET/g" -e "s/@CNC_PARTNER_SECRET@/$CNC_PARTNER_SECRET/g" -e "s/@CNC_PARTNER_ADMIN_SECRET@/$CNC_PARTNER_ADMIN_SECRET/g" -e "s/@REACH_INTERNAL_PARTNER_SECRET@/$REACH_INTERNAL_PARTNER_SECRET/g" -e "s/@REACH_INTERNAL_PARTNER_ADMIN_SECRET@/$REACH_INTERNAL_PARTNER_ADMIN_SECRET/g" -e "s/@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@/$ADMIN_SECRET/g" -e "s/@MONITORING_PROXY_ADMIN_SECRET@/$PARTNER_MONITORING_PROXY_ADMIN_SECRET/g" -e "s/@MONITORING_PROXY_SECRET@/$PARTNER_MONITORING_PROXY_SECRET/g" -e "s/@KMC_SSO_SERVER_ADMIN_SECRET@/$PARTNER_KMC_SSO_ADMIN_SECRET/g" -e "s/@KMC_SSO_SERVER_SECRET@/$PARTNER_KMC_SSO_SECRET/g" -e "s/@MONITOR_PARTNER_ADMIN_SECRET@/$MONITOR_PARTNER_ADMIN_SECRET/g" -e "s/@SERVICE_URL@/$SERVICE_URL/g" -e "s/@ADMIN_CONSOLE_ADMIN_MAIL@/$ADMIN_CONSOLE_ADMIN_MAIL/g" -e "s/@MONITOR_PARTNER_ADMIN_SECRET@/$MONITOR_PARTNER_ADMIN_SECRET/g"  -e "s/@MONITOR_PARTNER_SECRET@/$MONITOR_PARTNER_SECRET/g" -e "s/@PARTNER_ZERO_ADMIN_SECRET@/$PARTNER_ZERO_ADMIN_SECRET/g" -e "s/@BATCH_PARTNER_ADMIN_SECRET@/$BATCH_PARTNER_ADMIN_SECRET/g" -e "s/@MEDIA_PARTNER_ADMIN_SECRET@/$MEDIA_PARTNER_ADMIN_SECRET/g" -e "s/@TEMPLATE_PARTNER_ADMIN_SECRET@/$TEMPLATE_PARTNER_ADMIN_SECRET/g" -e "s/@HOSTED_PAGES_PARTNER_ADMIN_SECRET@/$HOSTED_PAGES_PARTNER_ADMIN_SECRET/g" -e "s/@ADMIN_CONSOLE_PASSWORD@/$ADMIN_CONSOLE_PASSWORD/g"  -e "s/@WWW_HOST@/$KALTURA_FULL_VIRTUAL_HOST_NAME/g" -e "s/@PLAY_PARTNER_ADMIN_SECRET@/$PLAY_PARTNER_ADMIN_SECRET/g"   -e "s/@TEMPLATE_PARTNER_ADMIN_PASSWORD@/$TEMPLATE_PARTNER_ADMIN_PASSWORD/g" -e "s/@PARTNER_ZERO_SECRET@/$PARTNER_ZERO_SECRET/g" -e "s/@BATCH_PARTNER_SECRET@/$BATCH_PARTNER_SECRET/g" -e "s/@ADMIN_CONSOLE_PARTNER_SECRET@/$ADMIN_CONSOLE_PARTNER_SECRET/g" -e "s/@HOSTED_PAGES_PARTNER_SECRET@/$HOSTED_PAGES_PARTNER_SECRER/g" -e "s/@MEDIA_PARTNER_SECRET@/$MEDIA_PARTNER_SECRET/g" -e "s/@PLAY_PARTNER_SECRET@/$PLAY_PARTNER_SECRET/g" -e "s/@TEMPLATE_PARTNER_SECRET@/$TEMPLATE_PARTNER_SECRET/g"  -e "s/@VOD_PACKAGER_HOST@/$VOD_PACKAGER_HOST/g" -e "s/@VOD_PACKAGER_PORT@/$VOD_PACKAGER_PORT/g" -e "s/@LIVE_PACKAGER_HOST@/$VOD_PACKAGER_HOST/g" -e "s/@LIVE_PACKAGER_PORT@/$VOD_PACKAGER_PORT/g"  -e "s/@IP_RANGE@/$IP_RANGE/g"  $TMPL > $DEST_FILE
#        sed -e "s#@STORAGE_BASE_DIR@#$BASE_DIR_WEB#g" -e "s#@WEB_DIR@#$BASE_DIR_WEB#g" $TMPL  > $DEST_FILE
done

for TMPL in `find .$INIT_DATA/ -name "*DeliveryProfile*"`;do
        echo $TMPL
        DEST_FILE=`echo $TMPL | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
        sed -e "s#@LIVE_PACKAGER_HOST@#$2#g" -e "s#@VOD_PACKAGER_HOST@#$3#g" -e "s#@WWW_HOST@#$4#g" $TMPL > $DEST_FILE
done

mkdir -p $BASE_DIR_LOG
#chmod 777 -R $BASE_DIR_LOG
LOG_TEMPLATE="server/configurations/logger.template.ini"
#LOG_TEMPLATE="configuration/logger.template.ini"
DEST_FILE=`echo $LOG_TEMPLATE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
echo $DEST_FILE
sed -e "s#@LOG_DIR@#$BASE_DIR_LOG#g" $LOG_TEMPLATE > $DEST_FILE




