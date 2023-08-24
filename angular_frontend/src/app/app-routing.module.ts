import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WindowComponent } from './window/window.component';

const routes: Routes = [
  { path: '', redirectTo: 'main-page', pathMatch: 'full' },
  { path: 'main-page', component: WindowComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
