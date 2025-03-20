import { Component, ComponentRef, Injectable, Type, ViewContainerRef } from '@angular/core';
import { ContainerComponent } from './container/container.component';
import { DropdownMenuComponent } from './dropdown-menu/dropdown-menu.component';
import { LabelComponent } from './label/label.component';
import { MenuBarComponent } from './menu-bar/menu-bar.component';
import { ButtonComponent } from './button/button.component';
import { CanvasComponent } from './canvas/canvas.component';
import { TextfieldComponent } from './textfield/textfield.component';
import { ModalComponent } from './modal/modal.component';
import { ProgressBarComponent } from './progress-bar/progress-bar.component';
import { CheckboxComponent } from './checkbox/checkbox.component';
import { CollapseComponent } from './collapse/collapse.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { TabsComponent } from './tabs/tabs.component';


@Injectable({
  providedIn: 'root'
})
export class ComponentCreationService {

  constructor() { }


  componentCreation(child: ViewContainerRef, key: string): ComponentRef<any> | null {

    let dict: { key: string, value: Type<any> }[] = [
      { key: "container", value: ContainerComponent },
      { key: "dropdown_menu", value: DropdownMenuComponent },
      { key: "label", value: LabelComponent },
      { key: "button", value: ButtonComponent },
      { key: "canvas", value: CanvasComponent },
      { key: "textfield", value: TextfieldComponent },
      { key: "modal", value: ModalComponent },
      { key: "progress_bar", value: ProgressBarComponent },
      { key: "checkbox", value: CheckboxComponent },
	  { key: "collapse", value: CollapseComponent },
	  { key: "sidebar", value: SidebarComponent },
	  { key: "tabs", value: TabsComponent },

    ]

    let component = null

    let index = dict.findIndex(item => item.key == key)
    if (index >= 0) {
      component = child.createComponent(dict[index].value)
    }

    if (component == null && key != "menu_bar" && key != "context_menu" && key != "message") {
      console.log("Could not associate component key with an component: " + key)
      //throw new Error("Could not associate component key with an component: " + key)
    }


    return component
  }
}

