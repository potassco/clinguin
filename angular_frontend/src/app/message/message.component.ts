import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { ElementDto } from '../types/json-response.dto';
import { CallBackHelperService } from '../callback-helper.service';
import { AttributeHelperService } from '../attribute-helper.service';

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.scss']
})
export class MessageComponent {
  @ViewChild("theMessage",{static:false}) theMessage! : ElementRef
  @Input() element: ElementDto | null = null

  attrType : string = ""
  attrMessage : string = ""
  attrTitle : string = ""

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      console.log(this.element)

      let htmlDdbut = this.theMessage.nativeElement

      let attrType = AttributeHelperService.findGetAttributeValue("type", this.element.attributes, "warning")
      let attrTitle = AttributeHelperService.findGetAttributeValue("title", this.element.attributes, "Title")
      let attrMessage = AttributeHelperService.findGetAttributeValue("message", this.element.attributes, "Message")

      if (attrType == "error") {
        attrType = "danger"
      }

      this.attrType = attrType
      this.attrTitle = attrTitle
      this.attrMessage = attrMessage



      this.cd.detectChanges()
    }
  }


}
