import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class Hl7Service {

  constructor(    private http: HttpClient) { }

  import(file,endpointName): any {

    const headers = new HttpHeaders()

    let host = location.host;
    let protocole = location.protocol

    //let base = protocole+'://'+host
    let base = 'http://localhost:52773'

    let path = endpointName.replace('fhir/r4','hl7')+'/'
 
    var result = this.http.post(base+path, file)
    return result
  }
}

