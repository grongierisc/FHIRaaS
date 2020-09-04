Class Interop.REST.CDA Extends %CSP.REST
{

Parameter CHARSET = "UTF-8";

Parameter CONVERTINPUTSTREAM = 1;

Parameter HandleCorsRequest = 1;

XData UrlMap [ XMLNamespace = "http://www.fhirhl7v2demo.com/urlmap" ]
{
<Routes>
  <Route Url="/:endpoint" Method="POST" Call="cda" Cors="true"/>
</Routes>
}

ClassMethod cda(endpoint As %String) As %Status
{
    set status = $$$OK

    Set tStream = %request.Content

    set tMsg = ##class(Ens.StreamContainer).%New(tStream)
    
    try {

        Set tBsName = "CDA_REST_"_endpoint

        $$$ThrowOnError(##class(Ens.Director).CreateBusinessService(tBsName,.tService))
        
        $$$ThrowOnError(tService.ProcessInput(tMsg,.output))

    } catch(ex) {
        set status = ex.AsStatus()
    }
    
    return status
}

}
