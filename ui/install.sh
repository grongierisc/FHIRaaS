#!/bin/sh
# $1 namespace $2 endpoint

rm -rf /usr/irissys/csp/healthshare/$1/$2
mkdir /usr/irissys/csp/healthshare/$1/$2

cp -R /opt/irisapp/ui /usr/irissys/csp/healthshare/$1/$2

old=__endpoint__ && \
new=v1/fhiraas/$1/fhir/r4/$2 && \
	sed -i "s|$old|$new|g" /usr/irissys/csp/healthshare/$1/$2/ui/index.html