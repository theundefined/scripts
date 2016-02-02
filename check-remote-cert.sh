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
	params="-noout -subject -issuer -dates -modulus"
fi

echo | openssl s_client -showcerts -connect ${SERVER} 2>/dev/null | # s_client connects
	openssl x509 $params
