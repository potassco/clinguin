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
  
  constructor(private componentService: ComponentResolutionService, private cd: ChangeDetectorRef, private attributeService: AttributeHelperService) {
  }

  ngAfterViewInit(): void {

    if (this.element != null) {

      let childLayout = this.attributeService.findGetAttributeValue("child_layout",this.element.attributes,"flex")

      this.element.children.forEach(item => {

        let my_comp = this.componentService.componentCreation(this.child, item.type)

        if (my_comp != null) {
          my_comp.setInput("element",item)
          let html: HTMLElement = <HTMLElement>my_comp.location.nativeElement
          html.id = item.id

          this.attributeService.addAttributes(html, item.attributes)
          this.attributeService.setAttributesDirectly(html, item.attributes)

          this.attributeService.setAbsoulteRelativePositions(childLayout, html, item)
          
          this.children.push(my_comp)
        }
      })

      this.cd.detectChanges()
    }
  }

}
