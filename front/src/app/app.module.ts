import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TenantsComponent } from './tenants/tenants.component';
import { EndpointsComponent } from './endpoints/endpoints.component';

import { ApiModule } from './fhiraas-api';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material-module';

import { NgxSpinnerModule } from "ngx-spinner";
import { AddComponent } from './tenants/add/add.component';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({ 
  declarations: [
    AppComponent,
    TenantsComponent,
    EndpointsComponent,
    AddComponent
  ],
  imports: [
    BrowserModule,  
    // import HttpClientModule after BrowserModule.  
    HttpClientModule,  
    MaterialModule,
    ApiModule,
    AppRoutingModule,
    NgxSpinnerModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
