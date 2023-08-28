import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { WindowComponent } from './window/window.component';
import { ContainerComponent } from './container/container.component';
import { DropdownMenuComponent } from './dropdown-menu/dropdown-menu.component';
import { NgbCollapseModule, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { RouterModule } from '@angular/router';
import { LabelComponent } from './label/label.component';
import { MenuBarComponent } from './menu-bar/menu-bar.component';
import { ButtonComponent } from './button/button.component';
import { CanvasComponent } from './canvas/canvas.component';
import { MessageComponent } from './message/message.component';
import { MainPageComponent } from './clingraphviz/main-page/main-page.component';
import { GraphOptionsComponent } from './clingraphviz/graph-options/graph-options.component';


@NgModule({
  declarations: [
    AppComponent,
    WindowComponent,
    ContainerComponent,
    DropdownMenuComponent,
    LabelComponent,
    MenuBarComponent,
    ButtonComponent,
    CanvasComponent,
    MessageComponent,
    MainPageComponent,
    GraphOptionsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    CommonModule,
    HttpClientModule,
    RouterModule,
    NgbModule,
    NgbCollapseModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
