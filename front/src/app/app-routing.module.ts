import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { EndpointsComponent } from './endpoints/endpoints.component';
import { TenantsComponent } from './tenants/tenants.component';

const routes: Routes = [
  { path: '', redirectTo: '/tenants', pathMatch: 'full' },
  { path: 'tenants/:id', component: EndpointsComponent },
  { path: 'tenants', component: TenantsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
