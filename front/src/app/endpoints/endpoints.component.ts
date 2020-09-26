import { Component, OnInit } from '@angular/core';
import { Tenant } from '../fhiraas-api/model/tenant';
import { Endpoint } from '../fhiraas-api/model/Endpoint';
import { ActivatedRoute } from '@angular/router';
import { DefaultService } from '../fhiraas-api';
import { Location } from '@angular/common';

@Component({
  selector: 'app-endpoints',
  templateUrl: './endpoints.component.html',
  styleUrls: ['./endpoints.component.scss']
})
export class EndpointsComponent implements OnInit {

  tenant : Tenant;
  endpoints : Endpoint[];
  endpoint : Endpoint;

  constructor(    
    private route: ActivatedRoute,
    private fhiraaService: DefaultService,
    private location: Location) {  }

  ngOnInit(): void {
    this.getTenant();
  }

  goBack(): void {
    this.location.back();
  }

  getTenant(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.fhiraaService.getTenant(id)
      .subscribe(tenant => this.tenant = tenant);
  }
}
