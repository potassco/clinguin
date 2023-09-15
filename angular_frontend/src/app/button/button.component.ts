import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';
import { ElementLookupService } from '../element-lookup.service';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss']
})
export class ButtonComponent {
  @ViewChild("theButton",{static:false}) theButton! : ElementRef

  @Input() element: ElementDto | null = null
  @Input() parentLayout: string = ""

  buttonLabel: string = ""
  disabledAttribute: boolean = false

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.setAttributes(this.element.attributes)
      let htmlDdbut = this.theButton.nativeElement
      this.callbackService.setCallbacks(htmlDdbut, this.element.do)

      this.cd.detectChanges()
    }
  }

  setAttributes(attributes : AttributeDto[]) {
      this.buttonLabel = this.attributeService.findGetAttributeValue("label",attributes,"")

      let htmlDdbut = this.theButton.nativeElement

      this.attributeService.setAttributesDirectly(htmlDdbut, attributes)
      this.attributeService.addAttributes(htmlDdbut, attributes)
      this.attributeService.textAttributes(htmlDdbut, attributes)
      this.attributeService.addGeneralAttributes(htmlDdbut, attributes)

      if (this.element != null) {
        this.attributeService.setAbsoulteRelativePositions(this.parentLayout, htmlDdbut, this.element)
      }

      let stringDisabled = this.attributeService.findGetAttributeValue("disabled", attributes, "false")
      if (stringDisabled == "false") {
        this.disabledAttribute = false
      } else if (stringDisabled == "true") {
        this.disabledAttribute = true
      } else {
        console.log("NOT SUPPORTED VALUE FOR DISABLED (assuming not disabled): ")
        console.log(stringDisabled)
        this.disabledAttribute = false
      }

      this.cd.detectChanges()
  }
}
