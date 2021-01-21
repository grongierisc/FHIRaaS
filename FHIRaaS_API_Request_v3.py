# -*- coding: utf-8 -*-

# Importation des modules
from FHIRaaS_Module.fhiraas_module import FHIRaaS_Module as FHIRaaS
import json
import os
import requests
from requests.auth import HTTPBasicAuth
from os import listdir
from os.path import isfile, join
import time

# Definition des variables nécessaires à la Basic Authentification
# Type de fichier
class FileType():
    CDA = "cda"
    HL7 = "hl7"
    FHIR = "fhir/r4"

port = "52773"
ip = "127.0.0.1" # localhost="127.0.0.1"
in_dir = "./in/"
out_dir = "./out/"
tenant = "Test"
tenants_list = ["Test", "Toast", "Tast"]
endpoint = "endpoint"
try:
    user = os.environ['USER']
    pwd =  os.environ['PASSWORD']

except:
    user = '_system'
    pwd = 'SYS'
file_type = FileType()

# Initialisation dans le script de FHIRaaS
fhiraas = FHIRaaS(ip=ip,port=port,user=user,pwd=pwd)


##########################
#    Fonction de Test    # 
##########################

# Test la fonction PUT tenant
# Retourne le message d'erreur associé à l'erreur rencontré
def test_putTenant(tenant=tenant):
    try:
        fhiraas.putTenant(tenant)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction GET tenant
def test_getTenant(tenant=tenant):
    try:
        fhiraas.getTenant(tenant)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction GET spec
def test_getSpec():
    try:
        fhiraas.getSpec()
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction DEL tenant
def test_delTenant(tenant=tenant):
    try:
        fhiraas.delTenant(tenant)
    except Exception as err:
        raise (Exception(str(err)))

# Test la fonction PUT tenant
def test_putTenant(tenant=tenant):
    try:
        fhiraas.putTenant(tenant)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction GET all tenant
def test_getTenants(tenants_list=tenants_list):
    try:
        for tenants in tenants_list:
            fhiraas.putTenant(tenants)
        time.sleep(10)
        fhiraas.getTenants()
        for tenants in tenants_list:
            fhiraas.delTenant(tenants)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction PUT tenant/endpoint
def test_putEndpoint(tenant=tenant,endpoint="lorem"):
    try:
        fhiraas.putTenant(tenant)
        time.sleep(10)
        fhiraas.putEndpoint(tenant, endpoint)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction GET tenant/endpoint
def test_getEndpoint(tenant=tenant,endpoint=endpoint):
    try:
        fhiraas.getEndpoint(tenant, endpoint)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction DEL tenant/endpoint
def test_delEndpoint(tenant, endpoint):
    try:
        fhiraas.delEndpoint(tenant, endpoint)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction POST patient (CDA) in tenant/endpoint
def test_postCDA(tenant, endpoint, file,file_type=file_type.CDA):
    try:
        fhiraas.postPatient(file, tenant, endpoint, file_type)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction POST patient (HL7) in tenant/endpoint
def test_postHL7(tenant, endpoint, file,file_type=file_type.HL7):
    try:
        fhiraas.postPatient(file, tenant, endpoint, file_type)
    except Exception as err:
        raise(Exception(str(err)))

# Test la fonction POST patient (FHIR) in tenant/endpoint
def test_postFHIR(tenant, endpoint, file,file_type=file_type.FHIR):
    try:
        fhiraas.postPatient(file, tenant, endpoint, file_type)
    except Exception as err:
        raise(Exception(str(err)))

def BasicTest(tenant=tenant, endpoint=endpoint):
    print("Lancement des Tests Basiques")
    nb_tests_S = 0
    nb_test_F = 0

    try:
        test_getSpec()
        nb_tests_S+=1
        print("SUCCESS || SINGLE || GET ||   SPEC   ")
    except Exception as err:
        print("FAILURE || SINGLE || GET ||   SPEC   \n" + str(err))
        nb_test_F+=1
    try:
        test_putTenant()
        nb_tests_S+=1
        time.sleep(10)
        print("SUCCESS || SINGLE || PUT ||  TENANT  ")
    except Exception as err:
        print("FAILURE || SINGLE || PUT ||  TENANT  \n" + str(err))
        nb_test_F+=1
    try:
        test_getTenant()
        nb_tests_S+=1
        print("SUCCESS || SINGLE || GET ||  TENANT  ")
    except Exception as err:
        print("FAILURE || SINGLE || GET ||  TENANT  \n" + str(err))
        nb_test_F+=1
    try:
        test_delTenant()
        nb_tests_S+=1
        print("SUCCESS || SINGLE || DEL ||  TENANT  ")
    except Exception as err:
        print("FAILURE || SINGLE || DEL ||  TENANT  \n" + str(err))
        nb_test_F+=1
    try:
        test_getTenants(tenants_list)
        nb_tests_S+=1
        print("SUCCESS || MULTI  || GET ||  TENANT  ")
    except Exception as err:
        print("FAILURE || SINGLE || GET ||  TENANT  \n" + str(err))
        nb_test_F+=1
    try:
        test_putEndpoint()
        print("SUCCESS || SINGLE || PUT || ENDPOINT ")
        nb_tests_S+=1
    except Exception as err:
        print("FAILURE || SINGLE || PUT || ENDPOINT \n" + str(err))
        nb_test_F+=1
    try:
        time.sleep(15)
        test_getEndpoint()
        nb_tests_S+=1
        print("SUCCESS || SINGLE || GET || ENDPOINT ")
    except Exception as err:
        print("FAILURE || SINGLE || GET || ENDPOINT \n" + str(err))
        nb_test_F+=1
    try:
        time.sleep(15)
        test_delEndpoint(tenant, endpoint="lorem")
        nb_tests_S+=1
        print("SUCCESS || SINGLE || DEL || ENDPOINT ")
    except Exception as err:
        print("FAILURE || SINGLE || DEL || ENDPOINT \n" + str(err))
        nb_test_F+=1
    fhiraas.delTenant("Test")

    print("\nNumber of tests : " + str(nb_tests_S + nb_test_F))
    print("Number of tests passed : " + str(nb_tests_S))
    print("Number of tests failed : " + str(nb_test_F))
    if nb_tests_S != (nb_test_F+nb_tests_S):
        return 84
    else:
        return 0

def main():
    return (BasicTest())

if __name__ == "__main__":
    main()