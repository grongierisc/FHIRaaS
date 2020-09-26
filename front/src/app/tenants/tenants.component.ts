import { Component, OnInit } from '@angular/core';
import { DefaultService } from '../fhiraas-api';
import { Tenant } from '../fhiraas-api/model/tenant';
import { PendingEndpoint } from '../fhiraas-api/model/PendingEndpoint';


@Component({
  selector: 'app-tenants',
  templateUrl: './tenants.component.html',
  styleUrls: ['./tenants.component.scss']
})
export class TenantsComponent implements OnInit {

  tenant : Tenant;
  tenants: Tenant[];
  pendingEndpoint : any;

  constructor(private fhiraaService: DefaultService) { }

  ngOnInit(): void {
    this.getTenants();
  }

  deleteTenant(tenant : Tenant){
    this.fhiraaService.deleteTenant(tenant.tenantId).subscribe(        
      res => {
        console.log(res);
      },
      error => {
        console.log(error);
      });
    this.getTenants();
  }
  

  addTenant(id: string): void {
    id = id.trim();
    if (!id) { return; }
    this.fhiraaService.putTenant(id)
      .subscribe(pendingEndpoint => {
        this.pendingEndpoint = pendingEndpoint;
      });
    this.getTenants();
  }

  getTenants(): void {
    this.fhiraaService.getTenants().subscribe(        
      tenants => {
          this.tenants = tenants
          },
          error => {
            console.log(error);
          })
    
  }

}
