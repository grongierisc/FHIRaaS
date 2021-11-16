ARG IMAGE=intersystemsdc/irishealth-community:2021.1.0.215.3-zpm
FROM $IMAGE

USER root

# prepare durability
RUN	mkdir -p /external/data && \
	chown -R ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /external && \
	chmod -R g+w /external

# prepare data
RUN	mkdir -p /data && \
	chown -R ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /data && \
	chmod -R g+w /data

WORKDIR /opt/irisapp
RUN chown ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /opt/irisapp
USER ${ISC_PACKAGE_MGRUSER}

COPY front/dist/FHIRaaS /usr/irissys/csp/fhiraas
COPY src src
COPY misc misc
COPY iris.script /tmp/iris.script

# run iris and initial 
RUN iris start $ISC_PACKAGE_INSTANCENAME \
	&& iris session $ISC_PACKAGE_INSTANCENAME < /tmp/iris.script \
	&& iris stop $ISC_PACKAGE_INSTANCENAME quietly

RUN old=http://localhost:52773/crud/_spec && \
	new=http://localhost:52773/fhiraas/v1/tenants/_spec && \
	sed -i "s|$old|$new|g" /usr/irissys/csp/swagger-ui/index.html
