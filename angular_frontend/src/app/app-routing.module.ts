import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WindowComponent } from './window/window.component';
import { NgbDropdownModule, NgbModule } from '@ng-bootstrap/ng-bootstrap';

const routes: Routes = [
  { path: '', redirectTo: 'main-page', pathMatch: 'full' },
  { path: 'main-page', component: WindowComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes), NgbModule],
  exports: [RouterModule]
})
export class AppRoutingModule { }
