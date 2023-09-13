import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { CallBackHelperService } from '../callback-helper.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.scss']
})
export class MessageComponent {
  @Input() element: ElementDto | null = null

  attrType : string = ""
  attrMessage : string = ""
  attrTitle : string = ""

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService : ElementLookupService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.setAttributes(this.element.attributes)

      this.cd.detectChanges()
    }
  }

  
  setAttributes(attributes: AttributeDto[]) {
    
      let attrType = this.attributeService.findGetAttributeValue("type", attributes, "warning")
      let attrTitle = this.attributeService.findGetAttributeValue("title", attributes, "Title")
      let attrMessage = this.attributeService.findGetAttributeValue("message", attributes, "Message")

      if (attrType == "error") {
        attrType = "danger"
      }

      console.log(attrType)

      this.attrType = attrType
      this.attrTitle = attrTitle
      this.attrMessage = attrMessage

      this.cd.detectChanges()
  }
}
