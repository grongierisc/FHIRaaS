#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importation des modules
import requests
import time
import json
from requests.auth import HTTPBasicAuth
import os

# Definition des variables nécessaires à la Basic Authentification

port = "52773"
ip = "127.0.0.1" # or localhost

# Type de fichier

CDA = "cda"
HL7 = "hl7"
FHIR = "fhir/r4"

try:
    user = os.environ['USER']
    pwd =  os.environ['PASSWORD']

except:
    print("Error: Invalid USER or PASSWORD")
    exit(84)

#######################################################################
                # Défintion des Fonctions  Requêtes #
#######################################################################

# Fait la requête PUT http://{ip}:{port}/fhiraas/v1/tenants/{tenant_name}
def put_tenant(tenant_name):
    #print("put : " + tenant_name)
    counter = 0
    post = "http://"+ip+":"+port+ "/fhiraas/v1/tenants" + '/' + tenant_name
    r = requests.put(post, auth=HTTPBasicAuth(user, pwd))
    time.sleep(8) # Dire pourquoi on sleep
    while ((str(r.json()["status"]) == "pending") and (counter < 15)): # Tant que la création du tenant n'est pas terminé il recommencera n fois la requête
        time.sleep(8)
        r = requests.put(post, auth=HTTPBasicAuth(user, pwd))
        counter+=1
    if (counter >= 15): # Si n fois dépasser -> ERREUR
        raise Exception("  --> " + post + "\n  --> Error: Time out")
    jsonResponse = r.json()
    if (r.status_code != 200): # Si le status code est différent de 200 -> ERREUR
        raise Exception("  --> " + post + "\n  --> Error: Expected 200 " + " but got " + str(r.status_code))
    if (jsonResponse["status"] != "running"): # Si le status est différent de "running" -> ERREUR
        raise Exception("  --> " + post + "\n  --> Error: Expected running " + " but got " + str(jsonResponse["status"]))
    if (jsonResponse["type"] != "endpoint"):  # Si le type est différent de "endpoint" -> ERREUR
        raise Exception("  --> " + post + "\n  --> Error: Expected endpoint " + " but got " + str(jsonResponse["type"]))
    if (jsonResponse["name"] != str("/v1/fhiraas/"+tenant_name+"/fhir/r4/endpoint").lower()): # Si le type est différent de "/v1/fhiraas/{tenant_name}/fhir/r4/endpoint" -> ERREUR
        raise Exception("  --> " + post + "\n  --> Error: Expected " + str("/v1/fhiraas/"+tenant_name+"/fhir/r4/endpoint").lower() + " but got " + str(jsonResponse["name"]))
    return r

# Fait la requête GET http://{ip}:{port}/fhiraas/v1/tenants/{tenant_name}
def get_tenant(tenant_name):
    #print("get : " + tenant_name)
    post = "http://"+ip+":"+port+ "/fhiraas/v1/tenants" + '/' + tenant_name
    r = requests.get(post, auth=HTTPBasicAuth(user, pwd))
    jsonResponse = r.json()
    if (r.status_code != 200):
        raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
    if (jsonResponse["tenantId"] != tenant_name):
        raise Exception("  --> " + post + "\n  --> Error: Expected " + " but got " + str(jsonResponse["tenantId"]))
    return r

# Fait la requête GET http://{ip}:{port}/fhiraas/v1/tenants/_spec
def get_spec():
    #print("get : spec")
    post = "http://"+ip+":"+port+ "/fhiraas/v1/tenants/_spec"
    r = requests.get(post, auth=HTTPBasicAuth(user, pwd))
    if (r.status_code != 200):
        raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
    return r

# Fait la requête GET http://{ip}:{port}/fhiraas/v1/tenants/
def get_all_tenants():
    #print("get : all")
    post = "http://"+ip+":"+port+ "/fhiraas/v1/tenants"
    r = requests.get(post, auth=HTTPBasicAuth(user, pwd))
    if (r.status_code != 200):
        raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
    return r

# Fait la requête DEL http://{ip}:{port}/fhiraas/v1/tenants/{tenant_name}
def del_tenant(tenant_name):
    #print("del : " + tenant_name)
    post = "http://"+ip+":"+port+ "/fhiraas/v1/tenants" + '/' + tenant_name
    r = requests.delete(post, auth=HTTPBasicAuth(user, pwd))
    if (r.status_code != 200):
        raise Exception("  --> " + post + "\n  --> Error: Expected 200 " + " but got " + str(r.status_code))
    return r

# Fait la requête PUT http://{ip}:{port}/fhiraas/v1/tenants/{tenant_name}/{endpoint_name}
def put_endpoint(tenant_name, endpoint_name):
    #print("put : " + tenant_name + '/' + endpoint_name)
    counter = 0
    post = "http://"+ip+":"+port+ "/fhiraas/v1/tenants" + '/' + tenant_name + '/' + endpoint_name
    r = requests.put(post, auth=HTTPBasicAuth(user, pwd))
    jsonResponse = r.json()
    time.sleep(8)
    while ((str(r.json()["status"]) != "running") and (counter < 15)): # Tant que la création du tenant n'est pas terminé il recommencera n fois la requête
        time.sleep(8)
        r = requests.put(post, auth=HTTPBasicAuth(user, pwd))
        counter+=1
    if (counter >= 15):
        raise Exception("  --> " + post + "\n  --> Error: Time out")
    if (r.status_code != 200):
        raise Exception("  --> " + post + "\n  --> Error: Expected 200 " + " but got " + str(r.status_code))
    if (jsonResponse["status"] != "running"):
        raise Exception("  --> " + post + "\n  --> Error: Expected running " + " but got " + str(jsonResponse["status"]))
    if (jsonResponse["type"] != "endpoint"):
        raise Exception("  --> " + post + "\n  --> Error: Expected endpoint " + " but got " + str(jsonResponse["type"]))
    if (jsonResponse["name"] != str("/v1/fhiraas/"+tenant_name+"/fhir/r4/").lower()+endpoint_name):
        raise Exception("  --> " + post + "\n  --> Error: Expected " + str("/v1/fhiraas/"+tenant_name+"/fhir/r4/").lower()+endpoint_name + " but got " + str(jsonResponse["name"]))
    return r

# Fait la requête GET http://{ip}:{port}/fhiraas/v1/tenants/{tenant_name}/{endpoint_name}
def get_endpoint(tenant_name, endpoint_name):
    #print("get : " + tenant_name + '/' + endpoint_name)
    counter = 0
    post = "http://"+ip+":"+port+ "/fhiraas/v1/tenants" + '/' + tenant_name + '/' + endpoint_name
    r = requests.get(post, auth=HTTPBasicAuth(user, pwd))
    while ((str(r.json()["status"]) != "complete") and (counter < 15)): # Tant que la création du tenant n'est pas terminé il recommencera n fois la requête
        time.sleep(8)
        r = requests.get(post, auth=HTTPBasicAuth(user, pwd))
        counter+=1
    if (counter >= 15):
        raise Exception("  --> " + post + "\n  --> Error: Time out")
    jsonResponse = r.json()
    if (r.status_code != 200):
        raise Exception("  --> " + post + "\n  --> Error: Expected 200 " + " but got " + str(r.status_code))
    if (jsonResponse["status"] != "complete"):
        raise Exception("  --> " + post + "\n  --> Error: Expected complete " + " but got " + str(jsonResponse["status"]))
    return r

# Fait la requête DEL http://{ip}:{port}/fhiraas/v1/tenants/{tenant_name}/{endpoint_name}
def del_endpoint(tenant_name, endpoint_name):
    #print("del : " + tenant_name + '/' + endpoint_name)
    post = "http://"+ip+":"+port+ "/fhiraas/v1/tenants" + '/' + tenant_name + '/' + endpoint_name
    r = requests.delete(post, auth=HTTPBasicAuth(user, pwd))
    if (r.status_code != 200):
        raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
    return r

def post_data(tenant_name, endpoint_name, file, file_type):
    post = "http://"+ip+":"+port+"/v1/fhiraas/"+tenant_name+"/"+file_type+"/"+endpoint_name+"/"
    data
    if file_type == CDA:
        header = {'Content-Type':'text/xml'}
        with open(file) as xml:
            data = xml
    elif file_type == HL7:
        header = {'Content-Type':'text/plain'}
        with open(file) as txt:
            data = txt
    elif file_type == FHIR:
        header = {'Content-Type': 'application/json'}
        with open(file) as json_file:
            json_data = json.load(json_file)
        data = json.dumps(json_data)
    else:
        raise Exception("  --> " + post + "\n  --> Error: hl7, cda, fhir" + " but got " + str(r.status_code))
    r = requests.post(post, auth=HTTPBasicAuth(user, pwd), headers=header, data=data)
    if (r.status_code != 200):
        raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
    return r

#####################################################################
                        # Sous-Fonction TEST #
            # Fonctions appelées dans les fonctions Test #
      # En cas d'erreur retourne le message d'erreur associé #
#####################################################################

# Test la fonction PUT tenant
# Retourne le message d'erreur associé à l'erreur rencontré
def test_put_tenant(tenant_name):
    try:
        put_tenant(tenant_name)
    except Exception as err:
        raise Exception(str(err))

# Test la fonction GET tenant
def test_get_tenant(tenant_name):
    try:
        get_tenant(tenant_name)
    except Exception as err:
        raise Exception(str(err))

# Test la fonction GET spec
def test_get_spec():
    try:
        get_spec()
    except Exception as err:
        raise Exception(str(err))

# Test la fonction DEL tenant
def test_del_tenant(tenant_name):
    try:
        del_tenant(tenant_name)
    except Exception as err:
        raise Exception(str(err))

# Test la fonction GET all tenants
def test_get_all_tenants(tenants = ["AZAP", "Carjack", "TWIY", "Miaouss"]):
    tenants.sort()
    i = 0
    try:
        for j in range(len(tenants)):
            test_put_tenant(tenants[j])
            time.sleep(8)
    except Exception as err:
        raise Exception(str(err))
        return
    time.sleep(5)
    r = get_all_tenants()
    if (r.status_code != 200):
        raise Exception(" --> Error: Expected 200" + " but got " + str(r.status_code))
    jsonResponse = r.json()
    for key in jsonResponse:
        if (str(key["tenantId"]) != tenants[i].upper()):
            raise Exception(" --> Error: Expected " + tenants[i].upper() + " but got " + str(key["tenantId"]))
        i+=1
    try:
        for j in range(len(tenants)):
            test_del_tenant(tenants[j])
    except Exception as err:
        raise Exception(str(err))

# Test la fonction PUT tenant/endpoint
def test_put_endpoint(tenant_name, endpoint_name):
    try:
        test_put_tenant(tenant_name)
    except Exception as err:
        raise Exception(str(err))
    time.sleep(2)
    try:
        put_endpoint(tenant_name, endpoint_name)
    except Exception as err:
        raise Exception(str(err))

# Test la fonction GET tenant/endpoint
def test_get_endpoint(tenant_name, endpoint_name):
    try :
        get_endpoint(tenant_name, endpoint_name)
    except Exception as err:
        print(str(err))
        raise Exception(str(err))

# Test la fonction DEL tenant/endpoint
def test_del_endpoint(tenant_name, endpoint_name):
    try:
        del_endpoint(tenant_name, endpoint_name)
    except Exception as err:
        raise Exception(str(err))

def test_post_cda(tenant_name, endpoint_name, file,file_type=CDA):
     try:
        post_data(tenant_name, endpoint_name, file, file_type)
    except Exception as err:
        raise Exception(str(err))

def test_post_hl7(tenant_name, endpoint_name, file,file_type=HL7):
     try:
        post_data(tenant_name, endpoint_name, file, file_type)
    except Exception as err:
        raise Exception(str(err))

def test_post_fhir(tenant_name, endpoint_name, file,file_type=FHIR):
     try:
        post_data(tenant_name, endpoint_name, file, file_type)
    except Exception as err:
        raise Exception(str(err))

########################################################################################
# Fonction qui réalise les tests basics
# Elle teste toutes les requêtes et vérifie si elle fonctionne
# Elle compte le nombre d'echec et de réussite et les affiche à la fin de son execution
########################################################################################

def Test_Basic(user = user, pwd = pwd, endpoints_list=["York", "Paris", "London"], tenants_list=["neque", "porro", "quisquam", "ipsum", "consectetur", "adipisci", "velit"]):
    nb_tests_S = 0
    nb_test_F = 0
    print("Basic Test for FHIRaaS :")
    #print("Test : GET spec")
    try:
        test_get_spec()
        nb_tests_S+=1
        print("SUCCESS || SINGLE || GET ||   SPEC   ")
    except Exception as err:
        print("FAILURE || SINGLE || GET ||   SPEC   \n" + str(err))
        nb_test_F+=1
    #print("Test : PUT a tenant named " + tenants_list[0])
    try:
        test_put_tenant(tenants_list[0])
        nb_tests_S+=1
        time.sleep(10)
        print("SUCCESS || SINGLE || PUT ||  TENANT  ")
    except Exception as err:
        print("FAILURE || SINGLE || GET ||  TENANT  \n" + str(err))
        nb_test_F+=1
    #print("Test : GET a tenant named " + tenants_list[0])
    try:
        test_get_tenant(tenants_list[0])
        nb_tests_S+=1
        print("SUCCESS || SINGLE || GET ||  TENANT  ")
    except Exception as err:
        print("FAILURE || SINGLE || GET ||  TENANT  \n" + str(err))
        nb_test_F+=1
    #print("Test : DEL a tenant named " + tenants_list[0])
    try:
        test_del_tenant(tenants_list[0])
        nb_tests_S+=1
        print("SUCCESS || SINGLE || DEL ||  TENANT  ")
    except Exception as err:
        print("FAILURE || SINGLE || DEL ||  TENANT  \n" + str(err))
        nb_test_F+=1
    #print("Test : GET all tenants")
    try:
        test_get_all_tenants(tenants_list[2:])
        nb_tests_S+=1
        print("SUCCESS || MULTI  || GET ||  TENANT  ")
    except Exception as err:
        print("FAILURE || SINGLE || DEL ||  TENANT  \n" + str(err))
        nb_test_F+=1
    #print("Test : PUT endpoint named \"YORK\" in the tenant \"ASAPS\"" + endpoints_list[0] + "in the tenant " + tenants_list[1])
    try:
        test_put_endpoint(tenants_list[1], endpoints_list[0])
        print("SUCCESS || SINGLE || PUT || ENDPOINT ")
        nb_tests_S+=1
    except Exception as err:
        print("FAILURE || SINGLE || PUT || ENDPOINT \n" + str(err))
        nb_test_F+=1
    #print("Test : GET endpoint named " + endpoints_list[0] + "in the tenant " + tenants_list[1])
    try:
        test_get_endpoint(tenants_list[1], endpoints_list[0])
        nb_tests_S+=1
        print("SUCCESS || SINGLE || GET || ENDPOINT ")
    except Exception as err:
        print("FAILURE || SINGLE || GET || ENDPOINT \n" + str(err))
        nb_test_F+=1
    #print("Test : DEL endpoint named " + endpoints_list[0] + "in the tenant " + tenants_list[1])
    try:
        time.sleep(15)
        test_del_endpoint(tenants_list[1], endpoints_list[0])
        nb_tests_S+=1
        print("SUCCESS || SINGLE || DEL || ENDPOINT ")
    except Exception as err:
        print("FAILURE || SINGLE || DEL || ENDPOINT " + str(err))
        nb_test_F+=1

    print("\nNumber of tests : " + str(nb_tests_S + nb_test_F))
    print("Number of tests passed : " + str(nb_tests_S))
    print("Number of tests failed : " + str(nb_test_F))
    if nb_tests_S != (nb_test_F+nb_tests_S):
        return 84
    else:
        return 0

########################################################
            # Tester le post de fichiers #
########################################################
def Test_post_data(user = user, pwd = pwd, endpoints_list=["York"], tenants_list=["Lorem"], path_to_sample="./FHIRaaS/misc/samples/"):
    try:
        test_put_tenant(tenants_list[0])
        test_put_endpoint(endpoints_list[0])
        test_post_fhir((tenants_list[0],endpoints_list[0],path_to_sample+"patient_bundle.json",FHIR)
    except Exception as err:
        print(str(err))
########################################################
                    # Execution #
########################################################

c = 0
#time.sleep(5)
req = requests.get("http://"+ip+":"+port+ "/fhiraas/v1/tenants/_spec", auth=HTTPBasicAuth(user, pwd))

while (req.status_code != 200 and c < 10): # Tant que la création du tenant n'est pas terminé il recommencera n fois la requête
        time.sleep(5)
        req = requests.get("http://"+ip+":"+port+ "/fhiraas/v1/tenants/_spec", auth=HTTPBasicAuth(user, pwd))
        print("WAITING FOR CONNECTION")
        c+=1
if c >= 10:
    print("TIMED OUT -> " + str(req.status_code))
    print(req)
    exit(84)
print("Connection to IRIS: SUCCES")

# Extraire les fichiers samples pour les tests


#
try:
    # Execute la Test_Basic
    #s = Test_Basic()
    Test_post_data()
except Exception as err:
    print(str(err))

# Affiche le temps d'execution du script
#print (time.clock() - start_time, "seconds")
exit(s)