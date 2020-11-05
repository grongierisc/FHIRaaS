#!/usr/bin/env python3
# Try the request modules for python with FHIRaaS API

import requests
import random
import time
from requests.auth import HTTPBasicAuth

user = '_system'
pwd = 'SYS'
tenant_names= ['zaez', 'aloowin', 'testas', 'dazingo']

def add_tenant(tenant_name):
    print("put : ", tenant_name)
    counter = 0
    r = requests.put("http://localhost:52773/fhiraas/v1/tenants" + '/' + tenant_name, auth=HTTPBasicAuth(user, pwd))
    time.sleep(5)
    while ((str(r.json()["status"]) == "pending") and (counter < 5)):
        time.sleep(2.5)
        r = requests.put("http://localhost:52773/fhiraas/v1/tenants" + '/' + tenant_name, auth=HTTPBasicAuth(user, pwd))
        counter+=1
    return r

def get_tenant(tenant_name):
    print("get : " + tenant_name)
    return requests.get("http://localhost:52773/fhiraas/v1/tenants" + '/' + tenant_name, auth=HTTPBasicAuth(user, pwd))

def get_spec():
    print("get : spec")
    return requests.get("http://localhost:52773/fhiraas/v1/tenants/_spec", auth=HTTPBasicAuth(user, pwd))

def get_all_tenants():
    print("get : all")
    return requests.get("http://localhost:52773/fhiraas/v1/tenants", auth=HTTPBasicAuth(user, pwd))

def del_tenant(tenant_name):
    print("del : " + tenant_name)
    return requests.delete("http://localhost:52773/fhiraas/v1/tenants" + '/' + tenant_name, auth=HTTPBasicAuth(user, pwd))

def add_endpoint(tenant_name, endpoint_name):
    print("put : " + tenant_name + '/' + endpoint_name)
    return requests.put("http://localhost:52773/fhiraas/v1/tenants" + '/' + tenant_name + '/' + endpoint_name, auth=HTTPBasicAuth(user, pwd))

def get_endpoint(tenant_name, endpoint_name):
    print("get : " + tenant_name + '/' + endpoint_name)
    return requests.get("http://localhost:52773/fhiraas/v1/tenants" + '/' + tenant_name + '/' + endpoint_name, auth=HTTPBasicAuth(user, pwd))

def del_endpoint(tenant_name, endpoint_name):
    print("del : " + tenant_name + '/' + endpoint_name)
    return requests.delete("http://localhost:52773/fhiraas/v1/tenants" + '/' + tenant_name + '/' + endpoint_name, auth=HTTPBasicAuth(user, pwd))

name = random.choice(tenant_names)
name = "ZAE"

#add_tenant("aloowin")
#get_tenant(name)
#get_spec()
del_tenant("ASAPS")
#get_all_tenants()
#add_endpoint(name, "AYA")
#get_endpoint("ASAPS", "YORK")
#del_endpoint("ASAPS", "YORK")

############################################################
                            #TEST#
############################################################

def test_put_tenant(tenant_name):
    r = add_tenant(tenant_name)
    jsonResponse = r.json()
    if (r.status_code != 200):
        raise Exception("Expected : 200 " + " but got : " + str(r.status_code))
    if (jsonResponse["status"] != "running"):
        raise Exception("Expected : running " + " but got : " + str(jsonResponse["status"]))
    if (jsonResponse["type"] != "endpoint"):
        raise Exception("Expected : endpoint " + " but got : " + str(jsonResponse["type"]))
    if (jsonResponse["name"] != str("/v1/fhiraas/"+tenant_name+"/fhir/r4/endpoint").lower()):
        raise Exception("Expected : " + str("/v1/fhiraas/"+tenant_name+"/fhir/r4/endpoint").lower() + " but got : " + str(jsonResponse["name"]))

def test_get_tenant(tenant_name):
    r = get_tenant(tenant_name)
    jsonResponse = r.json()
    exptd = "[{'name': '/v1/fhiraas/aloowin/fhir/r4/endpoint', 'enabled': True, 'service_config_data': {'fhir_metadata_set': 'HL7v40', 'fhir_version': '4.0.1', 'interactions_strategy_class': 'HS.FHIRServer.Storage.Json.InteractionsStrategy', 'default_search_page_size': 100, 'max_search_page_size': 100, 'max_search_results': 1000, 'max_conditional_delete_results': 3, 'fhir_session_timeout': 300, 'default_prefer_handling': 'lenient', 'debug_mode': 4}, 'csp_config': {'oauth_client_name': '', 'service_config_name': 'HS.FHIRServer.Interop.Service'}, 'interop_config': [{'service': 'HS.FHIRServer.Interop.Service', 'processes': '', 'operation': 'HS.FHIRServer.Interop.Operation'}, {'service': 'HS.FHIRServer.Interop.Service', 'processes': 'HS.FHIRServer.Interop.Operation', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'HS.FHIRServer.Interop.Service', 'processes': '', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'HL7_FILE_endpoint', 'processes': 'HL7_SDA_endpoint,SDA_FHIR_endpoint', 'operation': 'HS.FHIRServer.Interop.Operation'}, {'service': 'HL7_FILE_endpoint', 'processes': 'HL7_SDA_endpoint,SDA_FHIR_endpoint,HS.FHIRServer.Interop.Operation', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'HL7_FILE_endpoint', 'processes': 'HL7_SDA_endpoint,SDA_FHIR_endpoint', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'HL7_REST_endpoint', 'processes': 'HL7_SDA_endpoint,SDA_FHIR_endpoint', 'operation': 'HS.FHIRServer.Interop.Operation'}, {'service': 'HL7_REST_endpoint', 'processes': 'HL7_SDA_endpoint,SDA_FHIR_endpoint,HS.FHIRServer.Interop.Operation', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'HL7_REST_endpoint', 'processes': 'HL7_SDA_endpoint,SDA_FHIR_endpoint', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'CDA_FILE_endpoint', 'processes': 'CDA_SDA_endpoint,SDA_FHIR_endpoint', 'operation': 'HS.FHIRServer.Interop.Operation'}, {'service': 'CDA_FILE_endpoint', 'processes': 'CDA_SDA_endpoint,SDA_FHIR_endpoint,HS.FHIRServer.Interop.Operation', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'CDA_FILE_endpoint', 'processes': 'CDA_SDA_endpoint,SDA_FHIR_endpoint', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'CDA_REST_endpoint', 'processes': 'CDA_SDA_endpoint,SDA_FHIR_endpoint', 'operation': 'HS.FHIRServer.Interop.Operation'}, {'service': 'CDA_REST_endpoint', 'processes': 'CDA_SDA_endpoint,SDA_FHIR_endpoint,HS.FHIRServer.Interop.Operation', 'operation': 'HS.Util.Trace.Operations'}, {'service': 'CDA_REST_endpoint', 'processes': 'CDA_SDA_endpoint,SDA_FHIR_endpoint', 'operation': 'HS.Util.Trace.Operations'}]}]"
    if (r.status_code != 200):
        raise Exception("Expected : 200" + " but got : " + str(r.status_code))
    if (jsonResponse["tenantId"] != "aloowin"):
        raise Exception("Expected : " + " but got : " + str(jsonResponse["tenantId"]))
    if (str(jsonResponse["endpoints"]) != exptd):
        raise Exception("Expected : " + exptd + " but got : " + str(jsonResponse["endpoints"]))

def test_get_spec():
    r = get_spec()
    if (r.status_code != 200):
        raise Exception("Expected : 200" + " but got : " + str(r.status_code))

def test_del_tenant(tenant_name):
    r = del_tenant(tenant_name)
    if (r.status_code != 200):
        raise Exception("Expected : 200" + " but got : " + str(r.status_code))

def test_get_all_tenants(tenants = ["AZAP", "Carjack", "TWIY", "Miaouss"]):
    i = 0
    tenants.sort()
    try:
        test_put_tenant(tenants[0])
        time.sleep(2.5)
        test_put_tenant(tenants[1])
        time.sleep(2.5)
        test_put_tenant(tenants[2])
        time.sleep(2.5)
        test_put_tenant(tenants[3])
        time.sleep(2.5)
    except Exception as err:
        raise Exception("Expected OK but got KO : " + str(err))
        return
    time.sleep(5)
    r = get_all_tenants()
    if (r.status_code != 200):
        raise Exception("Expected : 200" + " but got : " + str(r.status_code))
    jsonResponse = r.json()
    for key in jsonResponse:
        if (str(key["tenantId"]) != tenants[i].upper()):
            raise Exception("Expected : " + tenants[i].upper() + " but got " + str(key["tenantId"]))
        i+=1
    try:
        test_del_tenant(tenants[0])
        test_del_tenant(tenants[1])
        test_del_tenant(tenants[2])
        test_del_tenant(tenants[3])
    except Exception as err:
        raise Exception("Expected OK but got KO : " + str(err))
    
def test_put_endpoint(tenant_name, endpoint_name):
    try:
        test_put_tenant(tenant_name)
    except Exception as err:
        raise Exception("Expected OK but got KO : " + str(err))
    time.sleep(2)
    r = add_endpoint(tenant_name, endpoint_name)
    jsonResponse = r.json()
    if (r.status_code != 200):
        raise Exception("Expected : 200 " + " but got : " + str(r.status_code))
    if (jsonResponse["status"] != "running"):
        raise Exception("Expected : running " + " but got : " + str(jsonResponse["status"]))
    if (jsonResponse["type"] != "endpoint"):
        raise Exception("Expected : endpoint " + " but got : " + str(jsonResponse["type"]))
    if (jsonResponse["name"] != str("/v1/fhiraas/"+tenant_name+"/fhir/r4/").lower()+endpoint_name):
        raise Exception("Expected : " + str("/v1/fhiraas/"+tenant_name+"/fhir/r4/").lower()+endpoint_name + " but got : " + str(jsonResponse["name"]))

def test_get_endpoint(tenant_name, endpoint_name):
    r = get_endpoint(tenant_name, endpoint_name)
    jsonResponse = r.json()
    if (r.status_code != 200):
        raise Exception("Expected : 200 " + " but got : " + str(r.status_code))
    if (jsonResponse["status"] != "running"):
        raise Exception("Expected : running " + " but got : " + str(jsonResponse["status"]))
    if (jsonResponse["type"] != "endpoint"):
        raise Exception("Expected : endpoint " + " but got : " + str(jsonResponse["type"]))
    if (jsonResponse["name"] != str("/v1/fhiraas/"+tenant_name+"/fhir/r4/").lower()+endpoint_name):
        raise Exception("Expected : " + str("/v1/fhiraas/"+tenant_name+"/fhir/r4/").lower()+endpoint_name + " but got : " + str(jsonResponse["name"]))

def test_del_endpoint(tenant_name, endpoint_name):
    r = del_endpoint(tenant_name, endpoint_name)
    if (r.status_code != 200):
        raise Exception("Expected : 200 " + " but got : " + str(r.status_code))

def Test(tenant_names = tenant_names, user = user, pwd = pwd):
    nb_tests_S = 0
    nb_test_F = 0
    print("Test : GET spec")
    try:
        test_get_spec()
        print("SUCCESS")
        nb_tests_S+=1
    except Exception as err:
        print("Error in \"GET spec\" \n==> ", err)
        nb_test_F+=1
    print("Test : PUT a tenant named aloowin")
    try:
        test_put_tenant("aloowin")
        print("SUCCESS")
        nb_tests_S+=1
        time.sleep(10)
    except Exception as err:
        print("Error in \"PUT a tenant named aloowin\" \n==> ",err)
        nb_test_F+=1
    print("Test : GET a tenant named aloowin")
    try:
        test_get_tenant("aloowin")
        print("SUCCESS")
        nb_tests_S+=1
    except Exception as err:
        print("Error in \"GET a tenant named aloowin\" \n==> ",err)
        nb_test_F+=1
    print("Test : DEL a tenant named aloowin")
    try:
        test_del_tenant("aloowin")
        print("SUCCESS")
        nb_tests_S+=1
    except Exception as err:
        print("Error in \"DEL a tenant named aloowin\" \n==> ",err)
        nb_test_F+=1
    print("Test : GET all tenants -> AZAP, Carjack, TWIY, Miaouss")
    try:
        test_get_all_tenants()
        print("SUCCESS")
        nb_tests_S+=1
    except Exception as err:
        print("Error in \"GET all tenants\" \n==> ",err)
        nb_test_F+=1
    print("Test : PUT endpoint named \"YORK\" in the tenant \"ASAPS\"")
    try:
        test_put_endpoint("ASAPS", "YORK")
        print("SUCCESS")
        nb_tests_S+=1
    except Exception as err:
        print("Error in \"PUT endpoint named \"YORK\" in the tenant \"ASAPS\" \" \n==> ",err)
        nb_test_F+=1
    print("Test : GET endpoint named \"YORK\" in the tenant \"ASAPS\"")
    try:
        test_get_endpoint("ASAPS", "YORK")
        print("SUCCESS")
        nb_tests_S+=1
    except Exception as err:
        print("Error in \"GET endpoint named \"YORK\" in the tenant \"ASAPS\" \" \n==> ",err)
        nb_test_F+=1
    print("Test : DEL endpoint named \"YORK\" in the tenant \"ASAPS\"")
    try:
        time.sleep(15)
        test_del_endpoint("ASAPS", "YORK")
        print("SUCCESS")
        nb_tests_S+=1
    except Exception as err:
        print("Error in \"DEL endpoint named \"YORK\" in the tenant \"ASAPS\" \" \n==> ",err)
        nb_test_F+=1

    print("Number of tests : ", nb_tests_S + nb_test_F)
    print("Number of tests passed : ", nb_tests_S)
    print("Number of tests failed : ", nb_test_F)


Test()