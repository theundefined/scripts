#!/bin/sh
SERVER=$1
if [ -z "$SERVER" ]; then
echo invoke:
echo $0 serwer:port
exit 0
fi
echo | openssl s_client -showcerts -connect ${SERVER} 2>/dev/null | # s_client connects
openssl x509 -noout -subject -issuer -dates -modulus
