import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TenantsComponent } from './tenants/tenants.component';
import { EndpointsComponent } from './endpoints/endpoints.component';

import { ApiModule } from './fhiraas-api';
import { HttpClientModule } from '@angular/common/http';

@NgModule({ 
  declarations: [
    AppComponent,
    TenantsComponent,
    EndpointsComponent
  ],
  imports: [
    BrowserModule,  
    // import HttpClientModule after BrowserModule.  
    HttpClientModule,  
    ApiModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
