import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';


@Component({
  selector: 'app-add',
  templateUrl: './add.component.html',
  styleUrls: ['./add.component.scss']
})
export class AddComponent implements OnInit {

  tenantForm: FormGroup;
  tenantId = '';
  hide : boolean = true;
  createEndpoint = new FormControl([{value:false}]);

  constructor(
  private fb: FormBuilder,
  private dialogRef: MatDialogRef<AddComponent>) {}

  ngOnInit(): void {
    this.tenantForm = this.fb.group({
      tenantId: [{value:''}, Validators.required],
      endpointName : [{value:'endpoint'}],
      endpointPassword : [{value:''}],
      createEndpoint : this.createEndpoint
    })
  }

  submit() {

    let newTenant: any = {
      tenantId: this.tenantForm.get('tenantId').value,
      createEndpoint : this.tenantForm.get('createEndpoint').value,
      endpointName : this.tenantForm.get('endpointName').value,
      endpointPassword : this.tenantForm.get('endpointPassword').value
    }
    
    this.dialogRef.close(newTenant)
  }

  getCreateEndpoint() : boolean{
    return this.createEndpoint.value;
  }

}
