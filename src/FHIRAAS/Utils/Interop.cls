Class FHIRAAS.API.Interop Extends HS.Util.Installer.Kit.Base
{

Parameter NamespaceTypes As %String;

ClassMethod Init(endpoint As %String) As %Status
{
    Quit ..ProductionModification(,endpoint,"FHIRItems",1) Quit:$$$ISERR(tSC)
}

ClassMethod Add(endpoint As %String) As %Status
{
	try {
		Set tSC=$$$OK
		Set tSC= ..ProductionModification(,endpoint,"HL7Items",1) Quit:$$$ISERR(tSC)
		$$$ThrowOnError(..CreateDirectoryItem("hl7",endpoint))
        Set tSC= ..ProductionModification(,endpoint,"SDAItems",1) Quit:$$$ISERR(tSC)
		$$$ThrowOnError(..CreateDirectoryItem("sda",endpoint))
        Set tSC= ..ProductionModification(,endpoint,"CDAItems",1) Quit:$$$ISERR(tSC)
		$$$ThrowOnError(..CreateDirectoryItem("cda",endpoint))
	} Catch ex {
		Set tSC=ex.AsStatus()
	}
	Quit tSC
}

ClassMethod ProductionModification(pNS As %String = {$namespace}, pEndpoint, pItems As %String = "", pUpdate As %Boolean = 0, pProductionClass = "", pAddItemsString = "") As %Status
{
	try {
		Set tSC=$$$OK
		Set tWhere = $Namespace Set:pNS]"" $Namespace=pNS
		Set tSC=..GetProduction(.tProdRef,pProductionClass) Quit:$$$ISERR(tSC)
		If pAddItemsString="" {
			Set tSC	= ..GetXDataAsStreamWithSubstitutions(pItems,pNS,pEndpoint, .tProduction) Quit:$$$ISERR(tSC)

		} Else {
			Set tProduction = ##class(%Stream.GlobalCharacter).%New()
			Do tProduction.Write("<Items>"_pAddItemsString_"</Items>"),tProduction.Rewind()
		}
		set tReader = ##class(%XML.Reader).%New()
		Set tSC = tReader.OpenStream(tProduction,.tObject) Quit:$$$ISERR(tSC)
		Do tReader.Correlate("Item","Ens.Config.Item")
		While tReader.Next(.tItem, .tSC) {
			Set tSC=..AddUpdateConfigItem(tItem,tProdRef,pUpdate) 
			Quit:$$$ISERR(tSC)
		}
		Set tSC=##class(HS.Util.Installer.Upgrade.Abstract).SaveProduction(tProdRef)
		
	} Catch ex {
		Set tSC=ex.AsStatus()
	}
	Set $Namespace=tWhere
	Quit tSC
}

ClassMethod GetXDataAsStreamWithSubstitutions(pXData, pNamespace, pEndpoint, ByRef pStream) As %Status
{
	If pXData'[":" Set pXData="xdata://"_$classname()_":"_pXData
	Set tSC = ##class(Ens.Util.URLStream).GetURLStream(pXData,.tStream) 
	If $$$ISERR(tSC) Quit tSC
	Do tStream.Rewind()
	Set tString=tStream.Read(30000000000)
	For  {
		Set tPos=$f(tString,"${")
		Quit:'tPos
		Set tPosEnd=$f(tString,"}",tPos)
		Quit:'tPosEnd
		Set name=$e(tString,tPos,tPosEnd-2)
		set value = $s(name="namespace":pNamespace,name="endpoint":pEndpoint,1:"default")
		Set tString=$e(tString,1,tPos-3)_value_$e(tString,tPosEnd,*)
	}
	Set pStream=##class(%Stream.GlobalCharacter).%New()
	Do pStream.Write(tString),pStream.Rewind()
	Quit tSC
}

ClassMethod CreateDirectoryItem(item As %String, endpoint As %String) As %Status
{
	set tPath = "/tmp/share/"_$namespace_"/"_item_"/in/"_endpoint_"/"
	$$$ThrowOnError(..CreateDirectory(tPath))

	set tPath = "/tmp/share/"_$namespace_"/"_item_"/out/"_endpoint_"/"
	$$$ThrowOnError(..CreateDirectory(tPath))

	set tPath = "/tmp/share/"_$namespace_"/"_item_"/tmp/"_endpoint_"/"
	$$$ThrowOnError(..CreateDirectory(tPath))

	Quit $$$OK
}

ClassMethod CreateDirectory(pPath As %String) As %Status
{
	set pPath=##class(%File).NormalizeDirectory(pPath)
	Quit ##class(%File).CreateDirectoryChain(pPath,.tErr)
}

XData HL7Items
{
<Items>
  <Item Name="HL7_FILE_${endpoint}" Category="Demo" ClassName="EnsLib.HL7.Service.FileService" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="MessageSchemaCategory">2.3.1</Setting>
    <Setting Target="Host" Name="TargetConfigNames">HL7_SDA_${endpoint}</Setting>
    <Setting Target="Adapter" Name="FilePath">/tmp/share/${namespace}/hl7/in/${endpoint}/</Setting>
    <Setting Target="Adapter" Name="ArchivePath">/tmp/share/${namespace}/hl7/out/${endpoint}/</Setting>
    <Setting Target="Adapter" Name="FileSpec">*.txt</Setting>
    <Setting Target="Adapter" Name="WorkPath">/tmp/share/${namespace}/hl7/tmp/${endpoint}/</Setting>
  </Item>
  <Item Name="HL7_SDA_${endpoint}" Category="" ClassName="Interop.HL7TransformProcess" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigNames">SDA_FHIR_${endpoint}</Setting>
  </Item>
</Items>
}

XData SDAItems
{
<Items>
  <Item Name="SDA_FHIR_${endpoint}" Category="" ClassName="HS.FHIR.DTL.Util.HC.SDA3.FHIR.Process" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="true" Schedule="">
    <Setting Target="Host" Name="TargetConfigName">HS.FHIRServer.Interop.Operation</Setting>
    <Setting Target="Host" Name="FHIREndpoint">/v1/fhiraas/${namespace}/fhir/r4/${endpoint}</Setting>
    <Setting Target="Host" Name="FHIRMetadataSet">HL7v40 / Base HL7 Metadata for FHIR R4 (4.0.1)</Setting>
    <Setting Target="Host" Name="FormatFHIROutput">1</Setting>
    <Setting Target="Host" Name="OutputToQuickStream">1</Setting>
    <Setting Target="Host" Name="TraceOperations">*FULL*</Setting>
  </Item>
</Items>
}

XData FHIRItems
{
<Items>
  <Item Name="HS.FHIRServer.Interop.Service" Category="" ClassName="HS.FHIRServer.Interop.Service" PoolSize="0" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TraceOperations">*FULL*</Setting>
  </Item>
  <Item Name="HS.FHIRServer.Interop.Operation" Category="" ClassName="HS.FHIRServer.Interop.Operation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
  </Item>
  <Item Name="HS.Util.Trace.Operations" Category="" ClassName="HS.Util.Trace.Operations" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
  </Item>
</Items>
}

XData CDAItems
{
<Items>
  <Item Name="CDA_FILE_${endpoint}" Category="" ClassName="EnsLib.File.PassthroughService" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Adapter" Name="ArchivePath">/tmp/share/${namespace}/cda/out/${endpoint}/</Setting>
    <Setting Target="Adapter" Name="FilePath">/tmp/share/${namespace}/cda/in/${endpoint}/</Setting>
    <Setting Target="Adapter" Name="WorkPath">/tmp/share/${namespace}/cda/tmp/${endpoint}/</Setting>
    <Setting Target="Host" Name="TargetConfigNames">CDA_SDA_${endpoint}</Setting>
  </Item>
  <Item Name="CDA_SDA_${endpoint}" Category="" ClassName="Interop.CCDATransformProcess" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="TargetConfigName">SDA_FHIR_${endpoint}</Setting>
  </Item>
</Items>
}

}
