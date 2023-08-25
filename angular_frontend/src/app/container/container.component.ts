import { ChangeDetectorRef, Component, Input, Type, ViewChild, ViewContainerRef } from '@angular/core';
import { ElementDto } from '../types/json-response.dto';
import { ComponentResolutionService } from '../component-resolution.service';
import { AttributeHelperService } from '../attribute-helper.service';

@Component({
  selector: 'app-container',
  templateUrl: './container.component.html',
  styleUrls: ['./container.component.scss']
})
export class ContainerComponent{
  @ViewChild('child',{read: ViewContainerRef}) child!: ViewContainerRef;
  @Input() element: ElementDto | null = null

  container_id: string = ""
  container: ElementDto | null = null

  children: any = []
  
  constructor(private cd: ChangeDetectorRef) {
  }

  ngAfterViewInit(): void {

    this.element?.children.forEach(item => {

      let my_comp = ComponentResolutionService.componentCreation(this.child, item.type)

      if (my_comp != null) {
        my_comp.setInput("element",item)
        let html: HTMLElement = <HTMLElement>my_comp.location.nativeElement
        html.id = item.id

        AttributeHelperService.addAttributes(html, item.attributes)
        AttributeHelperService.setAttributesDirectly(html, item.attributes)

        this.children.push(my_comp)

      }
    })

    this.cd.detectChanges()
  }

}
