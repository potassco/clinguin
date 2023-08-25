import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild, ViewRef } from '@angular/core';
import { ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';

@Component({
  selector: 'app-label',
  templateUrl: './label.component.html',
  styleUrls: ['./label.component.scss']
})
export class LabelComponent {
  @ViewChild('label',{static:true}) label! : ElementRef
  @Input() element: ElementDto | null = null

  elementLabel: string = ""

  constructor (private  cd: ChangeDetectorRef) {}


  ngAfterViewInit(): void {

    if (this.element != null) {
      console.log(this.element)
      let index = this.element.attributes.findIndex(attr => attr.key == "label")
      if (index >= 0) {
        this.elementLabel = this.element.attributes[index].value
      }

      let htmlDdbut = this.label.nativeElement

      AttributeHelperService.addAttributes(htmlDdbut, this.element.attributes)
      AttributeHelperService.textAttributes(htmlDdbut, this.element.attributes)
      AttributeHelperService.setAttributesDirectly(htmlDdbut, this.element.attributes)

      this.cd.detectChanges()
      /*


      this.element.children.forEach(child => {
        let index = child.attributes.findIndex(attr => attr.key == "label")
        if (index >= 0) {
          this.dropDownMenuItems.push({label:child.attributes[index].value, element:child})
        }
      })

      let htmlDdbut = this.ddbut.nativeElement

      AttributeHelperService.addAttributes(htmlDdbut, this.element.attributes)
      AttributeHelperService.textAttributes(htmlDdbut, this.element.attributes)

      let border_color = "black"
      index = this.element.attributes.findIndex(item => item.key == "border_color")
      if (index >= 0) {
          border_color = this.element.attributes[index].value
      }       
      htmlDdbut.style.borderColor = border_color

      this.cd.detectChanges()
      */
    }
  }

  /*
  onClick(element: ElementDto) {

    let callback : CallbackDto = element.callbacks[0]

    this.frontendService.policyPost(callback)
  }

  onDropdownChange() {
    if (this.element != null) {
      this.element.children.forEach(child => {
        let htmlChild : HTMLElement | null = document.getElementById(child.id)
        console.log(htmlChild)
        if (htmlChild != null) {
          AttributeHelperService.addAttributes(htmlChild, child.attributes)
          AttributeHelperService.textAttributes(htmlChild, child.attributes)
        }
      })
      this.cd.detectChanges()
    }
  }
  */
}

