import { Component, Injectable, Type, ViewContainerRef } from '@angular/core';
import { ContainerComponent } from './container/container.component';
import { DropdownMenuComponent } from './dropdown-menu/dropdown-menu.component';

@Injectable({
  providedIn: 'root'
})
export class ComponentResolutionService {

  constructor() { }


    static component_resolution(child: ViewContainerRef, key: string) {

        let component = null

        if (key == "container") {
            component = child.createComponent(ContainerComponent)
        }  else if (key == "dropdown_menu") {
            component = child.createComponent(DropdownMenuComponent)
        }

        return component
    }
}

