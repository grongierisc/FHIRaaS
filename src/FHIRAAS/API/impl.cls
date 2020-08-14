/// Iris Api to manage tenants<br/>
/// Business logic class defined by OpenAPI in FHIRAAS.API.spec<br/>
/// Created Aug 14, 2020 11:28:36
Class FHIRAAS.API.impl Extends %REST.Impl [ ProcedureBlock ]
{

/// If ExposeServerExceptions is true, then details of internal errors will be exposed.
Parameter ExposeServerExceptions = 1;

/// Return the list of available tenant on this Iris instance.
ClassMethod getTenants() As %DynamicObject
{
    #dim dyna as %DynamicArray
    set dyna = []

    set tTenant = ""
    While $order(^%SYS("HealthShare","Instances",tTenant))'="" {
        set tTenant = $order(^%SYS("HealthShare","Instances",tTenant))
        do:(tTenant'="FHIRAAS") dyna.%Push(tTenant)
    }


    Quit dyna
}

/// Returns a tenant by ID.<br/>
/// The method arguments hold values for:<br/>
///     tenantId, the tenant Id<br/>
ClassMethod getTenant(tenantId As %String) As %Stream.Object
{
    Quit ""
}

/// Create a tenant with an ID.<br/>
/// The method arguments hold values for:<br/>
///     tenantId, the tenant Id<br/>
///     tenantInformations<br/>
ClassMethod putTenant(tenantId As %String, tenantInformations As %Stream.Object) As %Stream.Object
{
    set sc = $$$OK

    Try {
        

        Set namespace=tenantId

        Set appKey = "/v1/fhir/"_tenantId_"/r4"
        Set strategyClass = "HS.FHIRServer.Storage.Json.InteractionsStrategy"
        Set metadataConfigKey = "HL7v40"

        //Install a Foundation namespace and change to it
        $$$ThrowOnError(##class(HS.HC.Util.Installer).InstallFoundation(namespace))

        zn namespace

        // Install elements that are required for a FHIR-enabled namespace
        Do ##class(HS.FHIRServer.Installer).InstallNamespace()

        // Install an instance of a FHIR Service into the current namespace
        do ##class(HS.FHIRServer.Installer).InstallInstance(appKey, strategyClass, metadataConfigKey,"",0)
	
	} Catch Error {
		zn "FHIRAAS"
        $$$ThrowOnError(Error.AsStatus())
	}

    zn "FHIRAAS"

    Quit ""
}

/// Delete a tenant with an ID.<br/>
/// The method arguments hold values for:<br/>
///     tenantId, the tenant Id<br/>
ClassMethod deleteTenant(tenantId As %String) As %Stream.Object
{
    set sc = $$$OK

    zn "%SYS"

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
		zn "FHIRAAS"
        $$$ThrowOnError(Error.AsStatus())
	}

    zn "FHIRAAS"

    Quit ""
}

}
