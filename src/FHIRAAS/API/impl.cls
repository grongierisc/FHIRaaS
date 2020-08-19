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
	
    Try {
        
        Set namespace=$zcvt(tenantId,"U")

        //Install a Foundation namespace and change to it
        $$$ThrowOnError(##class(HS.HC.Util.Installer).InstallFoundation(namespace))

        //Map Interop
        $$$ThrowOnError(##class(FHIRAAS.API.Utils).MapFHIRAASForNamespace(namespace))

        Return ..addEndpoint(tenantId,"endpoint")
	
	} Catch Error {

        $$$ThrowOnError(Error.AsStatus())
	}

    Quit ""
}

ClassMethod addEndpoint(tenantId As %String, endpoint As %String) As %Stream.Object
{
    New $namespace
    Set $namespace=tenantId

    // Install elements that are required for a FHIR-enabled namespace
    Do ##class(HS.FHIRServer.Installer).InstallNamespace()

    //Init default interop
    $$$ThrowOnError(##class(FHIRAAS.API.Interop).Init(endpoint))
    $$$ThrowOnError(##class(FHIRAAS.API.Interop).Add(endpoint))

    Set appKey = "/v1/fhiraas/"_tenantId_"/fhir/r4/"_endpoint
    Set strategyClass = "HS.FHIRServer.Storage.Json.InteractionsStrategy"
    Set metadataConfigKey = "HL7v40"

    // Install an instance of a FHIR Service into the current namespace
    set jobKey = ##class(HSMOD.REST.Async.API).RunInBackgroundAndReturnJobKey("HS.FHIRServer.Installer","InstallInstance",appKey, strategyClass, metadataConfigKey,"",0)
    
    Set $namespace="FHIRAAS"
    Set %response.ContentType = ..#CONTENTTYPEJSON
    Return ##class(FHIRAAS.API.Utils).GetJob(jobKey)
}

ClassMethod deleteEndpoint(tenantId As %String, endpoint As %String, delete As %Boolean = 1) As %Stream.Object
{
    New $namespace
    Set $namespace=tenantId

    // Install elements that are required for a FHIR-enabled namespace
    Do ##class(HS.FHIRServer.Installer).InstallNamespace()

    Set appKey = "/v1/fhiraas/"_tenantId_"/fhir/r4/"_endpoint

    // Install an instance of a FHIR Service into the current namespace
    do ##class(HS.FHIRServer.Installer).UninstallInstance(appKey,delete)
    
    Quit ""
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
