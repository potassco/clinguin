import { ChangeDetectorRef, Component, ElementRef, Inject, Input, ViewChild, ViewContainerRef } from '@angular/core';
import { CallbackDto, ElementDto } from '../types/json-response.dto';
import { DrawFrontendService } from '../draw-frontend.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { DOCUMENT } from '@angular/common';

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
  dropDownMenuItems : {label:string, element:ElementDto}[] = []

  constructor(private attributeService: AttributeHelperService, private  cd: ChangeDetectorRef, private frontendService: DrawFrontendService, @Inject(DOCUMENT) document: Document) {
  }


  ngAfterViewInit(): void {

    if (this.element != null) {
      let index = this.element.attributes.findIndex(attr => attr.key == "selected")
      if (index >= 0) {
        this.buttonLabel = this.element.attributes[index].value
      }

      this.element.children.forEach(child => {
        let index = child.attributes.findIndex(attr => attr.key == "label")
        if (index >= 0) {
          this.dropDownMenuItems.push({label:child.attributes[index].value, element:child})
        }
      })

      let htmlDdbut = this.ddbut.nativeElement

      this.attributeService.addAttributes(htmlDdbut, this.element.attributes)
      this.attributeService.textAttributes(htmlDdbut, this.element.attributes)
      this.attributeService.setAttributesDirectly(htmlDdbut, this.element.attributes)

      let border_color = "black"
      index = this.element.attributes.findIndex(item => item.key == "border_color")
      if (index >= 0) {
          border_color = this.element.attributes[index].value
      }       
      htmlDdbut.style.borderColor = border_color

      this.cd.detectChanges()
    }
  }

  onClick(element: ElementDto) {

    let callback : CallbackDto = element.callbacks[0]

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
