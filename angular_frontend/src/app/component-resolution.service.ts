import { Component, ComponentRef, Injectable, Type, ViewContainerRef } from '@angular/core';
import { ContainerComponent } from './container/container.component';
import { DropdownMenuComponent } from './dropdown-menu/dropdown-menu.component';
import { LabelComponent } from './label/label.component';

@Injectable({
  providedIn: 'root'
})
export class ComponentResolutionService {

  constructor() { }


    static componentCreation(child: ViewContainerRef, key: string): ComponentRef<any> | null {

        let dict : {key:string, value:Type<any>}[] = [
          {key:"container",value:ContainerComponent},
          {key:"dropdown_menu", value:DropdownMenuComponent},
          {key:"label", value:LabelComponent}
        ]

        let component = null
        
        let index = dict.findIndex(item => item.key == key)
        if (index >= 0) {
          // TODO
          component = child.createComponent(dict[index].value)
        }

        if (component == null) {
          //throw new Error("Could not associate component key with an component: " + key)
        }


        return component
    }
}

