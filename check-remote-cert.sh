#!/bin/sh
SERVER=$1
if [ -z "$SERVER" ]; then
echo invoke:
echo $0 serwer:port
exit 0
fi
if [ "$2" ]; then
	shift
	params=$*
else
	params="-noout -subject -issuer -dates -modulus -pubkey"
fi
SERVERNAME=$(echo $SERVER|cut -f 1 -d ':')

echo | openssl s_client -showcerts -servername ${SERVERNAME} -connect ${SERVER} 2>/dev/null | # s_client connects
	openssl x509 $params

# bin/check-remote-cert.sh google.com:443 -text |grep DNS |tr ', ' '\n\n' |grep DNS |cut -f 2 -d ':' |xargs echo
