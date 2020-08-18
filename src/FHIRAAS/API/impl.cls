/// Iris Api to manage tenants<br/>
/// Business logic class defined by OpenAPI in FHIRAAS.API.spec<br/>
/// Created Aug 14, 2020 11:28:36
Class FHIRAAS.API.impl Extends (%REST.Impl, %CSP.REST) [ ProcedureBlock ]
{

/// If ExposeServerExceptions is true, then details of internal errors will be exposed.
Parameter ExposeServerExceptions = 1;

Parameter CONTENTTYPEJSON As %String = "application/json";

/// Return the list of available tenant on this Iris instance.
ClassMethod getTenants() As %DynamicObject
{
    #dim dyna as %DynamicArray
    set dyna = []

    set tTenant = ""
    While $order(^%SYS("HealthShare","Instances",tTenant))'="" {
        set tTenant = $order(^%SYS("HealthShare","Instances",tTenant))
        if (tTenant'="FHIRAAS") {
            do dyna.%Push(..GetEndpointsByTenant(tTenant))
        }
    }

    Set %response.ContentType = ..#CONTENTTYPEJSON

    Quit dyna
}

/// Returns a tenant by ID.<br/>
/// The method arguments hold values for:<br/>
///     tenantId, the tenant Id<br/>
ClassMethod getTenant(tenantId As %String) As %Stream.Object
{
    set result = ""
    New $namespace
	
    Try {
        Set $namespace="%SYS"
        $$$ThrowOnError(##Class(Config.Namespaces).Get(tenantId))
        
        set result= ..GetEndpointsByTenant(tenantId)

    } Catch Error {

        $$$ThrowOnError(Error.AsStatus())
	}

    Set %response.ContentType = ..#CONTENTTYPEJSON

    Quit result
}

ClassMethod GetEndpointsByTenant(tenantId As %String) As %DynamicObject
{
    New $namespace
    Set $namespace=tenantId

    set result = {}
    set result.tenantId = tenantId
    set endpoints = []
    set list = ##class(HS.FHIRServer.API.InteractionsStrategy).GetEndpointInfo()
    
    set ptr = 0
    while $listnext(list, ptr, entry) {
        set endpoint = ##class(HS.FHIRServer.Config.RestHandler).SerializeEndpoint($listget(entry, 1))
        if endpoint '= "" {
            do endpoints.%Push(endpoint)
        }
    }
    set result.endpoints = endpoints


    set pendingEndpoints = ##class(HS.FHIRServer.Config.Setup).ReturnPendingEndpoints(1)
    if pendingEndpoints '= "" {
        set result.pendingEndpoints = pendingEndpoints
    } else {
        set result.pendingEndpoints = []
    }

	return result
}

/// Create a tenant with an ID.<br/>
/// The method arguments hold values for:<br/>
///     tenantId, the tenant Id<br/>
///     tenantInformations<br/>
ClassMethod putTenant(tenantId As %String, tenantInformations As %Stream.Object) As %Stream.Object
{
    set sc = $$$OK
    New $namespace
	
    Try {
        
        Set namespace=$zcvt(tenantId,"U")

        //Install a Foundation namespace and change to it
        $$$ThrowOnError(##class(HS.HC.Util.Installer).InstallFoundation(namespace))

        Set $namespace=namespace

        // Install elements that are required for a FHIR-enabled namespace
        Do ##class(HS.FHIRServer.Installer).InstallNamespace()

        Set name = "fhir"
        Set appKey = "/v1/fhiraas/"_tenantId_"/"_name_"/r4"
        Set strategyClass = "HS.FHIRServer.Storage.Json.InteractionsStrategy"
        Set metadataConfigKey = "HL7v40"

        // Install an instance of a FHIR Service into the current namespace
        set jobKey = ##class(HSMOD.REST.Async.API).RunInBackgroundAndReturnJobKey("HS.FHIRServer.Installer","InstallInstance",appKey, strategyClass, metadataConfigKey,"",0)
        
        Set $namespace="FHIRAAS"
        Set %response.ContentType = ..#CONTENTTYPEJSON
        Return ##class(FHIRAAS.API.Utils).GetJob(jobKey)
	
	} Catch Error {

        $$$ThrowOnError(Error.AsStatus())
	}

    Quit ""
}

/// Creates a new FHIRServer endpoint, or updates the existing one if already present.
/// The endpoint creation can take >1min, so it will be done async and return a job
/// reference that the client can poll for status
ClassMethod AddUpdateEndpointByTenant(tenantId As %String) As %Status
{

    New $namespace
    Set $namespace=tenantId

    set result = ""

	try {

        //if config is empty, put a default one
        if ($isobject(%request.Content)) {

            set endpoint = {}.%FromJSON(%request.Content)


        } else {
            
            set name = "fhir"
            Set appKey = "/v1/fhiraas/"_tenantId_"/"_name_"/r4"
            Set strategyClass = "HS.FHIRServer.Storage.Json.InteractionsStrategy"
            Set metadataConfigKey = "HL7v40"

            set endpoint = {}
            set endpoint.name = appKey
            set endpoint."service_config_data" = {}
            set endpoint."service_config_data"."interactions_strategy_class" = strategyClass
            set endpoint."service_config_data"."fhir_metadata_set" = metadataConfigKey

        }
		
		
		set name = endpoint.name
		set interactionsStrategy = endpoint."service_config_data"."interactions_strategy_class"
		set metadataSet = endpoint."service_config_data"."fhir_metadata_set"
		

		set output = {}
		
		//First check to see if the endpoint is currently being modified
		set pending = ##class(HS.FHIRServer.Config.Setup).ReturnPendingEndpoints(0, name, interactionsStrategy, metadataSet)
		if $isobject(pending) {
			set output.job = pending.%Get(0)
			return ..EmitResult(output)
		}
				
		if ' ##class(HS.FHIRServer.ServiceAdmin).EndpointExists(name) {
			//Note - currently Async call can't pass in objects, and the service config object is too long when serialized, so
			//we can't install and configure an endpoint in the same request *yet*. 
			set jobKey = ##class(HS.FHIRServer.Config.Setup).RunInBackgroundAndReturnJobKey("HS.FHIRServer.Installer", "InstallInstance", name, interactionsStrategy, metadataSet)
			set job = ##class(HS.FHIRServer.Config.Setup).JobRecordToJson(##class(HS.FHIRServer.Config.Setup).GetJobRecordFromKey(jobKey))
			set output.job = job
		}
		else {
			set strategy = ##class(HS.FHIRServer.API.InteractionsStrategy).GetStrategyForEndpoint(name)
			
			set configData = ##class(HS.FHIRServer.API.ConfigData).%New()
			$$$ThrowOnError(configData.%JSONImport(endpoint."service_config_data"))
			
			do strategy.SaveServiceConfigData(configData)
			
			set cspConfig = ##class(HS.Util.RESTCSPConfig).URLIndexOpen(endpoint.name)
			set cspConfig.ServiceConfigName = endpoint."csp_config"."service_config_name"
			set cspConfig.OAuthClientName = endpoint."csp_config"."oauth_client_name"
			$$$ThrowOnError(cspConfig.%Save())
			
			do strategy.SetEnabled(name, endpoint.enabled)
			
			set output.endpoint = ##class(HS.FHIRServer.Config.RestHandler).SerializeEndpoint(name)
		}

		Return ..EmitResult(output)
	}
	catch ex {
			$$$ThrowOnError(ex.AsStatus())
		}
	return result
}

/// Delete a tenant with an ID.<br/>
/// The method arguments hold values for:<br/>
///     tenantId, the tenant Id<br/>
ClassMethod deleteTenant(tenantId As %String) As %Stream.Object
{

    New $namespace
    Set $namespace="%SYS"

    Try {
        

        Set count = 0
        Set list = ""
        Set path = ""
        Set tRS = ##class(%Library.ResultSet).%New("Security.Applications:NamespaceList")
        Do tRS.Execute(tenantId)
        While tRS.Next() {
            Set count = count + 1
            if (count > 1) {
                Set list = list_","
                set path = path_","
            }
            Set list = list_tRS.Get("Name")
            Set path = path_tRS.Get("Path")
        }
        do tRS.Close()

		Set tSC = ##class(Config.Namespaces).Delete(tenantId)
		If $$$ISERR(tSC) throw ##Class(%Exception.StatusException).CreateFromStatus(tSC)
		
		#; clear application 
		If count > 0 {
			For n = 1:1:count {
				Set cspName = $PIECE(list,",",n)
                Set cspPath = $PIECE(path,",",n)
				#; delete csp application from security
				Set tSC = ##Class(Security.Applications).Delete(cspName)
                #; delete csp pages and physical path
				If (cspPath '= "") {
					#; delete csp pages in this directory
					Set tRS = ##class(%ResultSet).%New("%File:FileSet")
					Do tRS.Execute(cspPath,"*.csp")
					While tRS.Next() {
						Do ##class(%File).Delete(tRS.Get("Name"))
					}
					#; delete this directory - If there are no files left and no subdirectory, then it's deleted.
					Do ##class(%File).RemoveDirectory(cspPath)
				}
			}
		}
		
		#; remove Ensemble namespace
	 	If ((##class(%Library.EnsembleMgr).IsEnsembleInstalled() || ##class(%Library.EnsembleMgr).IsHealthShareInstalled())) {
	 		Set tSC = ##class(%Library.EnsembleMgr).DisableNamespace($ZCVT(tenantId,"U"))
	 		If $$$ISERR(tSC) throw ##Class(%Exception.StatusException).CreateFromStatus(tSC)
	 	}

        // Delete the database from the configuration file
        set del = 1
        If del = 1 {
            set dir = ##class(Config.Databases).GetDirectory(tenantId) 
            Set tSC = ##class(Config.Databases).Delete(tenantId)
            If $$$ISERR(tSC) throw ##Class(%Exception.StatusException).CreateFromStatus(tSC)
            
            // Delete the .DAT file
            Set tSC = ##class(SYS.Database).DeleteDatabase(dir)
            If $$$ISERR(tSC) throw ##Class(%Exception.StatusException).CreateFromStatus(tSC)
        }

	} Catch Error {
		
        $$$ThrowOnError(Error.AsStatus())
	}

    Quit ""
}

/// Prints <var>pPayload</var> if it is not empty, else sets the response status to be 'No Content' </br>
ClassMethod EmitResult(pPayload As %DynamicAbstractObject = "") As %DynamicAbstractObject
{
	#dim %response As %CSP.Response
	If pPayload = "" {
		Set %response.Status = ..#HTTP204NOCONTENT
	} Else {
		Set %response.ContentType = ..#CONTENTTYPEJSON
		return pPayload
	}
    Return {}
}

}
