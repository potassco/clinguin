import { APP_INITIALIZER, Injector, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { WindowComponent } from './window/window.component';
import { ContainerComponent } from './container/container.component';
import { DropdownMenuComponent } from './dropdown-menu/dropdown-menu.component';
import { NgbCollapseModule, NgbModal, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { LabelComponent } from './label/label.component';
import { MenuBarComponent } from './menu-bar/menu-bar.component';
import { ButtonComponent } from './button/button.component';
import { CanvasComponent } from './canvas/canvas.component';
import { MessageComponent } from './message/message.component';
import { MainPageComponent } from './clingraphviz/main-page/main-page.component';
import { GraphOptionsComponent } from './clingraphviz/graph-options/graph-options.component';
import { ConfigService } from './config.service';
import { LocatorService } from './locator.service';
import { TextfieldComponent } from './textfield/textfield.component';
import { ModalComponent } from './modal/modal.component';
import { ContextMenuComponent } from './context-menu/context-menu.component';
import { ProgressBarComponent } from './progress-bar/progress-bar.component';
import { CheckboxComponent } from './checkbox/checkbox.component';

function initialize() {
  return (): Promise<boolean> => {
    return new Promise<boolean>((resolve: (a: boolean) => void): void => { resolve(true); })
  }
}

export function appConfigInit(appConfigService: ConfigService) {
  return () => {
    return appConfigService.load()
  };
}

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
    GraphOptionsComponent,
    TextfieldComponent,
    ModalComponent,
    ContextMenuComponent,
    ProgressBarComponent,
    CheckboxComponent
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    FormsModule,
    CommonModule,
    HttpClientModule,
    NgbModule,
    NgbCollapseModule,
  ],
  providers: [{
    provide: APP_INITIALIZER,
    useFactory: appConfigInit,
    deps: [
      ConfigService
    ],
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(private injector: Injector) {
    LocatorService.injector = injector
  }
}
