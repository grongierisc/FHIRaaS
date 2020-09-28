import { Component, OnInit } from '@angular/core';
import { DefaultService } from '../fhiraas-api';
import { Tenant } from '../fhiraas-api/model/tenant';
import { PendingEndpoint } from '../fhiraas-api/model/pendingEndpoint';
import { flatMap } from 'rxjs/operators';
import { interval } from 'rxjs';
import { MatDialog} from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NgxSpinnerService } from "ngx-spinner"; 
import { AddComponent } from './add/add.component';
import { AddEndpointComponent } from '../endpoints/add/add.endpoint.component';


@Component({
  selector: 'app-tenants',
  templateUrl: './tenants.component.html',
  styleUrls: ['./tenants.component.scss']
})
export class TenantsComponent implements OnInit {

  tenant : Tenant;
  tenants: Tenant[];
  pendingEndpoints : PendingEndpoint[];
  polling :boolean = false;

  constructor(
    private fhiraaService: DefaultService,
    private spinnerService: NgxSpinnerService,
    public _dialog: MatDialog, 
    private _snackBar: MatSnackBar) {
    this.pendingEndpoints = new Array();
   }

  ngOnInit(): void {
    this.getTenants();
  }

  deleteTenant(tenant : Tenant){
    this.spinnerService.show();  
    this.fhiraaService.deleteTenant(tenant.tenantId).subscribe(        
      res => {
        this.spinnerService.hide();  
        this._snackBar.open(tenant.tenantId+' deleted!','Close', {
          duration: 5000
        });
        console.log(res);
        this.getTenants();
      },
      error => {
        console.log(error);
      });
      this.tenants = this.tenants.filter(obj => obj !== tenant);
  }
  

  addTenant(id: string): void {
    id = id.trim();
    if (!id) { return; }
    this.spinnerService.show();  
    this.fhiraaService.putTenant(id)
      .subscribe(pendingEndpoint => {
        this.spinnerService.hide();  
        this.pendingEndpoints.push(pendingEndpoint);
        this.getTenants();
        this._snackBar.open(id+' created!','Close', {
          duration: 5000
        });
      },
      error => {
        console.log(error);
      });
  }

  addEndpoint(tenantId: string,endpointId: string): void {
    tenantId = tenantId.trim();
    if (!tenantId) { return; }
    this.spinnerService.show();  
    this.fhiraaService.putEndpoint(tenantId,endpointId)
      .subscribe(pendingEndpoint => {
        this.spinnerService.hide();  
        this.pendingEndpoints.push(pendingEndpoint);
        this.getTenants();
        this._snackBar.open(endpointId+' created!','Close', {
          duration: 5000
        });
      },
      error => {
        console.log(error);
      });
  }

  getTenants(): void {
    this.fhiraaService.getTenants().subscribe(        
      tenants => {
          this.tenants = tenants;
          if (this.pendingEndpoints.length > 0 && !this.polling) {
            this.pollingEndpoints();
          };
          },
          error => {
            console.log(error);
          });

  }

  pollingEndpoints() :void {
    this.polling = true;
    let poll$ = interval(2500)
    .pipe(
        flatMap(() => this.fhiraaService.getTenants())
    )
    .subscribe(        
      tenants => {
          this.pendingEndpoints = new Array();
          tenants.forEach(tenant => {
            tenant.pendingEndpoints.forEach(pendingEndpoint => {
              this.pendingEndpoints.push(pendingEndpoint);
            });
          if (this.pendingEndpoints.length === 0) {
            this.polling = false;
            poll$.unsubscribe();
            this.tenants = tenants;
          }
          });
          },
          error => {
            console.log(error);
          });

  }

  openAddDialog(): void {
    const dialogRef = this._dialog.open(AddComponent, {
      panelClass: 'modal-panel',
      width: '700px',
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.addTenant(result.tenantId);
      }
    });
  }

  openAddEndpointDialog(tenant:Tenant): void {
    const dialogRef = this._dialog.open(AddEndpointComponent, {
      panelClass: 'modal-panel',
      width: '700px',
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.addEndpoint(tenant.tenantId,result.endpointName);
      }
    });
  }

}
