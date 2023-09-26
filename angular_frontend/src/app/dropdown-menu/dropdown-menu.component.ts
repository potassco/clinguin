import { ChangeDetectorRef, Component, ElementRef, Inject, Input, ViewChild, ViewContainerRef } from '@angular/core';
import { AttributeDto, WhenDto, ElementDto } from '../types/json-response.dto';
import { DrawFrontendService } from '../draw-frontend.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { DOCUMENT } from '@angular/common';
import { ElementLookupService } from '../element-lookup.service';
import { LocatorService } from '../locator.service';
import { CallBackHelperService } from '../callback-helper.service';

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

  constructor(private attributeService: AttributeHelperService, private  cd: ChangeDetectorRef, private frontendService: DrawFrontendService, @Inject(DOCUMENT) document: Document, private elementLookupService: ElementLookupService, private callbackHelperService: CallBackHelperService) {
  }


  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.element.children.forEach(child => {

        let childLabel = this.attributeService.findGetAttributeValue("label",child.attributes,"")

        let childObject = new DropdownMenuItemChild(childLabel, child)

        this.elementLookupService.addElementObject(child.id, childObject, child)

        this.dropDownMenuItems.push(childObject)

        this.cd.detectChanges()

        let htmlChild : HTMLElement | null = document.getElementById(child.id)
        if (htmlChild != null) {
          childObject.setHtmlElement(htmlChild)
          childObject.setAttributes(child.attributes)

          this.callbackHelperService.setCallbacks(htmlChild, child.when)

          let icon = htmlChild.children.item(0)
  
          if (icon != null) {
      
            this.attributeService.class(icon, child.attributes, ["fa"], 'icon')
          }
          
        }

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
    this.attributeService.class(htmlDdbut, attributes, ["btn"])

    htmlDdbut.style.border_color = this.attributeService.findGetAttributeValue("border_color", attributes, "black")

    this.cd.detectChanges()
  
  }

  onClick(element: ElementDto) {

    let callback : WhenDto = element.when[0]

    this.frontendService.policyPost(callback)
  }
}

class DropdownMenuItemChild {
  label!:string 
  element!:ElementDto
  htmlElement: HTMLElement | null = null

  constructor(label: string, element: ElementDto) {
    this.label = label
    this.element = element
  }

  setHtmlElement(htmlElement : HTMLElement) {
    this.htmlElement = htmlElement
  }

  setAttributes(attributes: AttributeDto[]) {
    if (this.htmlElement != null) {
      let attributeService = LocatorService.injector.get(AttributeHelperService)
      attributeService.addAttributes(this.htmlElement, attributes)
      attributeService.textAttributes(this.htmlElement, attributes)
      attributeService.setAttributesDirectly(this.htmlElement, attributes)
      attributeService.class(this.htmlElement, attributes, ["dropdown-item"])
      
    }
  }
}
