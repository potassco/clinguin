import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { CallBackHelperService } from '../callback-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { AttributeHelperService } from '../attribute-helper.service';

@Component({
  selector: 'app-textfield',
  templateUrl: './textfield.component.html',
  styleUrls: ['./textfield.component.scss']
})
export class TextfieldComponent {
  @ViewChild("theTextfield",{static:false}) theTextfield! : ElementRef

  @Input() element: ElementDto | null = null
  @Input() parentLayout: string = ""

  placeholder: string = ""

  disabledAttribute: boolean = false
  inputType: string = "text"

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.setAttributes(this.element.attributes)
      let htmlTextfield = this.theTextfield.nativeElement
      this.callbackService.setCallbacks(htmlTextfield, this.element.when)

      this.cd.detectChanges()
    }
  }

  setAttributes(attributes : AttributeDto[]) {

      this.placeholder = this.attributeService.findGetAttributeValue("placeholder", attributes, "")
      
      this.inputType = this.attributeService.findGetAttributeValue("input_type", attributes, "text")

      //this.buttonLabel = this.attributeService.findGetAttributeValue("label",attributes,"")

      let htmlTextfield = this.theTextfield.nativeElement

      this.attributeService.setAttributesDirectly(htmlTextfield, attributes)
      this.attributeService.addAttributes(htmlTextfield, attributes)
      this.attributeService.textAttributes(htmlTextfield, attributes)
      this.attributeService.addGeneralAttributes(htmlTextfield, attributes)
      this.attributeService.addClasses(htmlTextfield, attributes,[],[])

      if (this.element != null) {
        this.attributeService.setAbsoulteRelativePositions(this.parentLayout, htmlTextfield, this.element)
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
