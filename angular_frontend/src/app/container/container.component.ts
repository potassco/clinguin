import { ChangeDetectorRef, Component, Input, Type, ViewChild, ViewContainerRef } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { ComponentCreationService } from '../component-creation.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { ChildBearerService } from '../child-bearer.service';

@Component({
  selector: 'app-container',
  templateUrl: './container.component.html',
  styleUrls: ['./container.component.scss']
})
export class ContainerComponent{
  @ViewChild('child',{read: ViewContainerRef}) child!: ViewContainerRef;
  @Input() element: ElementDto | null = null
  @Input() parentLayout: string = ""

  container_id: string = ""
  container: ElementDto | null = null

  children: any = []
  
  constructor(private childBearerService: ChildBearerService, private cd: ChangeDetectorRef, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService) {
  }

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      let childLayout = this.attributeService.findGetAttributeValue("child_layout",this.element.attributes,"flex")

      this.element.children.forEach(item => {

        let my_comp = this.childBearerService.bearChild(this.child, item, childLayout)
        if (my_comp != null) {

          this.children.push(my_comp)
        }
      })

      this.cd.detectChanges()
    }
  }

  setAttributes(attributes: AttributeDto[]) {
    // Nothing to set here.
  }

}
