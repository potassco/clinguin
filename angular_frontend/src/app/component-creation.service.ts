import { Component, ComponentRef, Injectable, Type, ViewContainerRef } from '@angular/core';
import { ContainerComponent } from './container/container.component';
import { DropdownMenuComponent } from './dropdown-menu/dropdown-menu.component';
import { LabelComponent } from './label/label.component';
import { MenuBarComponent } from './menu-bar/menu-bar.component';
import { ButtonComponent } from './button/button.component';
import { CanvasComponent } from './canvas/canvas.component';
import { MainPageComponent } from './clingraphviz/main-page/main-page.component';
import { TextfieldComponent } from './textfield/textfield.component';
import { ModalComponent } from './modal/modal.component';

@Injectable({
  providedIn: 'root'
})
export class ComponentCreationService {

  constructor() { }


    componentCreation(child: ViewContainerRef, key: string): ComponentRef<any> | null {

        let dict : {key:string, value:Type<any>}[] = [
          {key:"container",value:ContainerComponent},
          {key:"dropdown_menu", value:DropdownMenuComponent},
          {key:"label", value:LabelComponent},
          {key:"button", value:ButtonComponent},
          {key:"canvas", value:CanvasComponent},
          {key:"clingraph_interactive", value: MainPageComponent},
          {key:"textfield", value: TextfieldComponent},
          {key:"modal", value: ModalComponent}
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

