import { Component, Injectable, Type, ViewContainerRef } from '@angular/core';
import { ContainerComponent } from './container/container.component';

@Injectable({
  providedIn: 'root'
})
export class ComponentResolutionService {

  constructor() { }


    static component_resolution(child: ViewContainerRef, key: string) {

        let component = null

        if (key == "container") {
            component = child.createComponent(ContainerComponent)
        } 

        return component

        /*
        let dict = [
            {key:"container",value: ContainerComponent},
            {key:"test",value: IntermediateComponentComponent}
        ]

        let index = dict.findIndex(item => item.key == key)

        let return_class =  null

        if (index >= 0) {
            return_class = dict[index].value
        } 

        return return_class
        */
    }
}

