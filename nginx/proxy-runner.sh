#!/bin/bash

set -e

echo "Checking for dhparams.pem"
if [ ! -f "/vol/proxy/ssl-dhparams.pem" ]; then
  echo "dhparams.pem does not exist - creating it"
  openssl dhparam -out /vol/proxy/ssl-dhparams.pem 2048
fi

# Avoid replacing these with envsubst
export host=\$host
export request_uri=\$request_uri

echo "Checking for fullchain.pem"
if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
  echo "fullchain.pem does not exist - creating it"
  certbot certonly --webroot -w /var/www/certbot -d ${DOMAIN} --agree-tos --email ${EMAIL} --no-eff-email --force-renewal
fi
  echo "Copying nginx.conf"
  envsubst < /etc/nginx/nginx.conf> /etc/nginx/conf.d/default.conf

nginx -g 'daemon off;'
