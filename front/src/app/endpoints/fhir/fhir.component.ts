import { Component, Inject, OnInit } from '@angular/core';
import { FhirClient } from 'ng-fhir/FhirClient';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Endpoint } from 'src/app/fhiraas-api';

@Component({
  selector: 'app-fhir',
  templateUrl: './fhir.component.html',
  styleUrls: ['./fhir.component.scss']
})
export class FhirComponent implements OnInit {

  private client: FhirClient;
  private endpoint : Endpoint;

  private config: any ;

  public conformance: any = {};
  public patients : any = {};

  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { 

    this.endpoint = data.packages;
    this.config = {
      'baseUrl': 'http://localhost:52773'+this.endpoint.name,
      'credentials': 'same-origin',
    };
    this.client = new FhirClient(this.config);

    this.client.conformance({}).then((response) => {
      if(response.data){
        this.conformance = (response.data || []);
      }
    }, (err) => {
      console.log(err);
    });

    this.client.search({type: 'Patient', query: {}}).then((response) => {
      if(response.data){
        this.patients = (response.data.entry || []);
      }
    }, (err) => {
      console.log(err);
    });
  }

  ngOnInit(): void {
  }

  stringify(obj: any): string{
    return JSON.stringify(obj,null,'  ');
  }

}
