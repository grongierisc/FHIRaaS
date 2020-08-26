## TODO 

- [x] HTTPS 
- [x] Generation de tenant en mode async
- [x] Affiner get tenants/:id
- [x] Ajouter l'interopérabilité (CCDA,HL7,SDA)
- [x] Ajouter information production dans json
- [x] Ajouter les mots de passe par tenant
- [x] Ajouter des tests unitaires

# Introduction 
This is the FHIR as a Service project (aka : FHIRAAS). It is based on InterSystem's IRIS for Health.
It's purpose is to create a ready to go SaaS plateform to generated FHIR endpoint with interoperability.
All can be done throw REST endpoint defined in misc/iris-api-operations.json

# Getting Started
1. Build this project, cf Build
2. The endpoint is : http://localhost:52773/fhiraas/v1/tenants
3. Create a tenant : POST http://localhost:52773/fhiraas/v1/tenants/{tenantName}
4. Tenant inforamtion : GET http://localhost:52773/fhiraas/v1/tenants/{tenantName}
5. The endpoint of the tenant is here : http://localhost:52773/v1/fhiraas/{tenantName}/fhir/r4/endpoint

# Build 
Run the server

```sh
docker-compose up -d
```

# Create tenant
The creation of a tenant and its endpoint is long.
For that, the Rest API is asynchronous.
When you will create a tenant you will recive this kind of response
```json
{
    "job_key": "NjczfHwx",
    "status": "running",
    "type": "endpoint",
    "name": "/v1/fhiraas/{tenantName}/fhir/r4/endpoint"
}
```
This mean the endpoint is running for creation.
To check if the endpoint is still in creation GET http://localhost:52773/fhiraas/v1/tenants/{tenantName}
```json
{
    "tenantId": "{tenantName}",
    "endpoints": [],
    "pendingEndpoints": [
        {
            "job_key": "NjczfHwx",
            "status": "running",
            "type": "endpoint",
            "name": "/v1/fhiraas/{tenantName}/fhir/r4/endpoint"
        }
    ]
}
```
When over endpoints array will be populated :
```json
{
    "tenantId": "{tenantName}",
    "endpoints": [
        {
            "name": "/v1/fhiraas/{tenantName}/fhir/r4/endpoint",
            "enabled": true,
            "service_config_data": {
                "fhir_metadata_set": "HL7v40",
                "fhir_version": "4.0.1",
                "interactions_strategy_class": "HS.FHIRServer.Storage.Json.InteractionsStrategy",
                "default_search_page_size": 100,
                "max_search_page_size": 100,
                "max_search_results": 1000,
                "max_conditional_delete_results": 3,
                "fhir_session_timeout": 300,
                "default_prefer_handling": "lenient",
                "debug_mode": 0
            },
            "csp_config": {
                "oauth_client_name": "",
                "service_config_name": "HS.FHIRServer.Interop.Service"
            }
        }
    ],
    "pendingEndpoints": []
}
```

# Misc
Visual Studio Directory Structure

```
.
├── misc
│   ├── samples
│   │   └── hl7 and cda examples
...
├── share
│   ├── tenantId
│   │   ├── cda, hl7, sda
│   │   │   └── list of in, out, tmp directories
...
├── src
│   ├── FHIRAAS
│   │   ├── API     //API for FHIRAAS
│   │   ├── Utils   //Helper methodes
│   │   ├── HS      //Fix for SDA -> FHIR
│   │   └── Interop //Interop specific developement
...
```

 ## Test this module
 
 Natively from depot :
 
 ```objectscript
 do ##class(%UnitTest.Manager).DebugRunTestCase("","Test.Grongier.JSON.Utils",,)
 ```

