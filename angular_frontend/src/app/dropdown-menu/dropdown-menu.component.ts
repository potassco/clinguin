import { ChangeDetectorRef, Component, ElementRef, Inject, Input, ViewChild, ViewContainerRef } from '@angular/core';
import { AttributeDto, DoDto, ElementDto } from '../types/json-response.dto';
import { DrawFrontendService } from '../draw-frontend.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { DOCUMENT } from '@angular/common';
import { ElementLookupService } from '../element-lookup.service';

@Component({
  selector: 'app-dropdown-menu',
  templateUrl: './dropdown-menu.component.html',
  styleUrls: ['./dropdown-menu.component.scss']
})
export class DropdownMenuComponent {
  // Why does the dropdown need this?
  @Input() element : ElementDto | null = null
  @Input() parentLayout: string = ""

  @ViewChild('ddbut', {static:true}) ddbut! : ElementRef

  buttonLabel : string = ""
  dropDownMenuItems : DropdownMenuItemChild[] = []

  constructor(private attributeService: AttributeHelperService, private  cd: ChangeDetectorRef, private frontendService: DrawFrontendService, @Inject(DOCUMENT) document: Document, private elementLookupService: ElementLookupService) {
  }


  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.element.children.forEach(child => {

        let childLabel = this.attributeService.findGetAttributeValue("label",child.attributes,"")

        let childObject = new DropdownMenuItemChild(childLabel, child)

        this.elementLookupService.addElementObject(child.id, childObject, child)

        this.dropDownMenuItems.push(childObject)
      })

      this.cd.detectChanges()
      
      this.setAttributes(this.element.attributes)
    }
  }

  setAttributes(attributes: AttributeDto[]) {

    let buttonLabel = this.attributeService.findAttribute("selected", attributes)
    if (buttonLabel != null) {
      this.buttonLabel = buttonLabel.value
    }
    
    let htmlDdbut = this.ddbut.nativeElement

    this.attributeService.addAttributes(htmlDdbut, attributes)
    this.attributeService.textAttributes(htmlDdbut, attributes)
    this.attributeService.setAttributesDirectly(htmlDdbut, attributes)

    htmlDdbut.style.border_color = this.attributeService.findGetAttributeValue("border_color", attributes, "black")

    this.cd.detectChanges()
  
  }

  onClick(element: ElementDto) {

    let callback : DoDto = element.do[0]

    this.frontendService.policyPost(callback)
  }

  onDropdownChange() {
    if (this.element != null) {
      this.element.children.forEach(child => {
        let htmlChild : HTMLElement | null = document.getElementById(child.id)
        if (htmlChild != null) {
          this.attributeService.addAttributes(htmlChild, child.attributes)
          this.attributeService.textAttributes(htmlChild, child.attributes)
          this.attributeService.setAttributesDirectly(htmlChild, child.attributes)
        }
      })
      this.cd.detectChanges()
    }
  }
}

class DropdownMenuItemChild {
  label!:string 
  element!:ElementDto

  constructor(label: string, element: ElementDto) {
    this.label = label
    this.element = element
  }

  setAttributes(attributes: AttributeDto[]) {
    console.log("TODO!!!")
  }
}
