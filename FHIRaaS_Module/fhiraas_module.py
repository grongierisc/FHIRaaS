
# -*- coding: utf-8 -*-

# Importation des modules
import requests
import time
import json
from requests.auth import HTTPBasicAuth
import os
from os import listdir
from os.path import isfile, join


CDA = "cda"
HL7 = "hl7"
FHIR = "fhir/r4"
user='_system' 
pwd='SYS'

# Definition de la classe

class FHIRaaS_Module():
    """
    module is made for doing request on a IRIS database using FHIRaaS API
    """
    __tenant_list = []
    __endpoint = ""
    __file_type = []
    __user = ""
    __pwd = ""
    __ip = ""
    __port = ""

    def __init__(self, ip="127.0.0.1", port="52773", user=user, pwd=pwd):
        self.__tenant_list = []
        self.endpoint = "endpoint"
        self.__file_type = ["cda", "hl7", "fhir/r4"]
        try:
            self.__user = os.environ['USER']
            self.__pwd = os.environ['PASSWORD']
        except:
            self.__user = user
            self.__pwd = pwd
        self.__ip = ip
        self.__port = port

    # Definine all getter
    def _getBaseURL(self):
        """
        get the basic URL Ex:-> http://localhost:52773/fhiraas/v1/
        """
        baseURL = 'http://'+self.__ip+':'+self.__port
        return baseURL

    def _getTenant(self, index=0):
        """
        get the tenant at index
        """
        return self.__tenant_list[index]

    def _getallTenant(self):
        """
        get the tenant at index
        """
        return self.__tenant_list

    def _getEndpoint(self):
        """
        get the endpoint
        """
        return self.__endpoint

    # Define all setter
    def _setTenant(self, tenant):
        """
        add a tenant to the tenant list
        """
        self.__tenant_list.append(tenant)

    def _setEndpoint(self, endpoint):
        """
        set a new endpoint
        """
        self.endpoint = endpoint

    def _setIP(self, ip):
        """
        set a new ip
        """
        self.__ip = ip

    def _setPort(self, port):
        """
        set a new port
        """
        self.__port

    def _setUser(self, user):
        """
        set a new user
        """
        self.__user = user

    def _setUser(self, pwd):
        """
        set a new password
        """
        self.__user = pwd

    # Define all request methods
    def getSpec(self):
        """
        execute the request GET the swagger
        """
        post = self._getBaseURL()+'/fhiraas/v1/'+"tenants" + '/' + "_spec"
        r = requests.get(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
        if (r.status_code != 200):
            raise Exception(
                "  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
        return r

    def putTenant(self, tenant_name):
        """
        execute the request PUT a tenant
        """
        self._setTenant(tenant_name)
        post = self._getBaseURL()+'/fhiraas/v1/'+"tenants" + '/' + tenant_name
        r = requests.put(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
        time.sleep(8)  # Dire pourquoi on sleep
        jsonResponse = r.json()
        if (r.status_code != 200):  # Si le status code est différent de 200 -> ERREUR
            raise Exception(
                "  --> " + post + "\n  --> Error: Expected 200 " + " but got " + str(r.status_code))
        # Si le type est différent de "endpoint" -> ERREUR
        if (jsonResponse["type"] != "endpoint"):
            raise Exception("  --> " + post + "\n  --> Error: Expected endpoint " +
                            " but got " + str(jsonResponse["type"]))
        # Si le type est différent de "/v1/fhiraas/{tenant_name}/fhir/r4/endpoint" -> ERREUR
        if (jsonResponse["name"] != str("/v1/fhiraas/"+tenant_name+"/fhir/r4/endpoint").lower()):
            raise Exception("  --> " + post + "\n  --> Error: Expected " + str("/v1/fhiraas/" +
                                                                               tenant_name+"/fhir/r4/endpoint").lower() + " but got " + str(jsonResponse["name"]))
        return r

    def getTenant(self, tenant_name):
        """
        execute the request GET a tenant
        """
        post = self._getBaseURL()+'/fhiraas/v1/'+"tenants" + '/' + tenant_name
        r = requests.get(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
        jsonResponse = r.json()
        if (r.status_code != 200):
            raise Exception(
                "  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
        if (jsonResponse["tenantId"] != tenant_name):
            raise Exception("  --> " + post + "\n  --> Error: Expected " + " but got " + str(jsonResponse["tenantId"]))
        return r

    def getTenants(self):
        """
        execute the request GET all tenants
        """
        post = self._getBaseURL()+'/fhiraas/v1/'+"tenants"
        r = requests.get(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
        if (r.status_code != 200):
            raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
        return r

    def delTenant(self, tenant_name):
        """
        execute the request DEL a tenant
        """
        post = self._getBaseURL()+'/fhiraas/v1/'+"tenants" + '/' + tenant_name
        r = requests.delete(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
        if (r.status_code != 200):
            raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
        return r

    def putEndpoint(self, tenant_name, endpoint_name):
        """
        execute the request PUT a enpoint
        """
        counter = 0
        self._setEndpoint(endpoint_name)
        post = self._getBaseURL()+'/fhiraas/v1/'+"tenants" + '/' + tenant_name + '/' + endpoint_name
        r = requests.put(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
        if (r.status_code != 200):
            raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
        jsonResponse = r.json()
        if (jsonResponse["status"] != "running" and jsonResponse["status"] != "pending"):
            raise Exception("  --> " + post + "\n  --> Error: Expected running " + " but got " + str(jsonResponse["status"]))
        time.sleep(8)  # Dire pourquoi on sleep
        return r

    def getEndpoint(self, tenant_name, endpoint_name):
        """
        execute the request GET a endpoint
        """
        counter = 0
        post = self._getBaseURL()+'/fhiraas/v1/'+"tenants" + '/' + tenant_name + '/' + endpoint_name
        r = requests.get(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
        if (r.status_code != 200):
            raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
        while ((str(r.json()["status"]) != "complete") and (counter < 35)): # Tant que la création du tenant n'est pas terminé il recommencera n fois la requête
            time.sleep(8)
            r = requests.get(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
            counter+=1
        if (counter >= 15):
            raise Exception("  --> " + post + "\n  --> Error: Time out")
        jsonResponse = r.json()
        if (r.status_code != 200):
            raise Exception("  --> " + post + "\n  --> Error: Expected 200 " + " but got " + str(r.status_code))
        if (jsonResponse["status"] != "complete"):
            raise Exception("  --> " + post + "\n  --> Error: Expected complete " + " but got " + str(jsonResponse["status"]))
        return r

    def delEndpoint(self, tenant_name, endpoint_name):
        """
        execute the request DEL a endpoint
        """
        post = self._getBaseURL()+'/fhiraas/v1/'+"tenants" + '/' + tenant_name + '/' + endpoint_name
        self._setEndpoint("endpoint")
        r = requests.delete(post, auth=HTTPBasicAuth(self.__user, self.__pwd))
        if (r.status_code != 200):
            raise Exception("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
        return r

    def postPatient(self, file,tenant_name, endpoint_name, file_type=FHIR):
        """
        execute the request POST a patient
        """
        data = open(file,'rb').read() # récupération du fichier
        post = self._getBaseURL()+'/v1/fhiraas/' + tenant_name+"/"+file_type+"/"+endpoint_name+"/" # création de l'url pour la requête
        if file_type == CDA: # si le fichier est un CDA sélectionne le header approprié au CDA
            header = {'Content-Type':'text/xml'} # si le fichier est un HL7 sélectionne le header approprié au HL7
        elif file_type == HL7:
            header = {'Content-Type':'text/plain'} 
        elif file_type == FHIR: # si le fichier est un FHIR sélectionne le header approprié au FHIR
            header = {'Content-Type': 'application/fhir+json; charset=UTF-8'}
        else: # En cas d'erreur le programme quitte
            raise Exception("  --> " + post + "\n  --> Error: hl7, cda, fhir" + " but got " + str('none'))
        r = requests.post(post, auth=HTTPBasicAuth(self.__user, self.__pwd), headers=header, data=data)
        del data
        if (r.status_code != 200): # Si la requête échoue le programme print l'erreur et passera au fichier suivant
            print("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
            return (0)
        else: # Si la reqête fonctionne le fichier sera déplacé dans le out_directory
            return (1)

    def putPatient(self, file,tenant_name, endpoint_name, file_type=FHIR):
        """
        execute the request PUT a patient
        """
        if file.lower().endswith(('.json','.xml','.hl7')) == False:
            return (0)
        data = open(file,'rb').read() # récupération du fichier
        post = self._getBaseURL()+'/v1/fhiraas/' + tenant_name+"/"+file_type+"/"+endpoint_name+"/"+"Patient/" # création de l'url pour la requête
        if file_type == CDA: # si le fichier est un CDA sélectionne le header approprié au CDA
            header = {'Content-Type':'text/xml'}
            return 0 # si le fichier est un HL7 sélectionne le header approprié au HL7
        elif file_type == HL7:
            header = {'Content-Type':'text/plain'}
            return 0 
        elif file_type == FHIR: # si le fichier est un FHIR sélectionne le header approprié au FHIR
            header = {'Content-Type': 'application/fhir+json; charset=UTF-8'}
            with open(file) as json_file:
                temp = json.load(json_file)
                if "id" in temp:
                    id = temp["id"]
                else:
                    print("Error : No ID found")
                    return 0
        else: # En cas d'erreur le programme quitte
            raise Exception("  --> " + post + "\n  --> Error: hl7, cda, fhir" + " but got " + str('none'))
        r = requests.put(post+id, auth=HTTPBasicAuth(self.__user, self.__pwd), headers=header, data=data)
        del data
        if (r.status_code != 200 and r.status_code != 201): # Si la requête échoue le programme print l'erreur et passera au fichier suivant
            print("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
            return (0)
        else: # Si la reqête fonctionne le fichier sera déplacé dans le out_directory
            return (1)

    def getRessource(self, RessourceType, tenant_name, endpoint_name, file_type=FHIR, id=""):
        """
        execute the request POST a patient
        """
        post = self._getBaseURL()+'/v1/fhiraas/' + tenant_name+"/"+file_type+"/"+endpoint_name+"/"+RessourceType+'/' # création de l'url pour la requête
        if id == "":
            post = post+id
        if file_type == CDA: # si le fichier est un CDA sélectionne le header approprié au CDA
            header = {'Content-Type':'text/xml'} # si le fichier est un HL7 sélectionne le header approprié au HL7
        elif file_type == HL7:
            header = {'Content-Type':'text/plain'} 
        elif file_type == FHIR: # si le fichier est un FHIR sélectionne le header approprié au FHIR
            header = {'Content-Type': 'application/fhir+json; charset=UTF-8'}
        else: # En cas d'erreur le programme quitte
            raise Exception("  --> " + post + "\n  --> Error: hl7, cda, fhir" + " but got " + str('none'))
        r = requests.get(post, auth=HTTPBasicAuth(self.__user, self.__pwd), headers=header)
        if (r.status_code != 200): # Si la requête échoue le programme print l'erreur et passera au fichier suivant
            print("  --> " + post + "\n  --> Error: Expected 200" + " but got " + str(r.status_code))
        return(r)
