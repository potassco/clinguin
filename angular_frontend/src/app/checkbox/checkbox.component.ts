import {ChangeDetectorRef, Component, ElementRef, Input, ViewChild} from '@angular/core';
import {AttributeDto, ElementDto} from "../types/json-response.dto";
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { CallBackHelperService } from "../callback-helper.service";

@Component({
  selector: 'app-checkbox',
  templateUrl: './checkbox.component.html',
  styleUrls: ['./checkbox.component.scss']
})
export class CheckboxComponent {
  @ViewChild('checkbox',{static:false}) checkbox! : ElementRef

  @Input() element: ElementDto | null = null

  checkboxID: string = crypto.randomUUID();
  checkboxLabel: string = ""
  disabledAttribute: boolean = false

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService) {}

  ngAfterViewInit(): void {
    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.setAttributes(this.element.attributes)
      let htmlDdbut = this.checkbox.nativeElement
      this.callbackService.setCallbacks(htmlDdbut, this.element.when)

      this.cd.detectChanges()
    }
  }

  setAttributes(attributes : AttributeDto[]) {
    this.checkboxLabel = this.attributeService.findGetAttributeValue("label",attributes,"")

    let htmlDdbut = this.checkbox.nativeElement

    this.attributeService.setAttributesDirectly(htmlDdbut, attributes)
    this.attributeService.addAttributes(htmlDdbut, attributes)
    this.attributeService.textAttributes(htmlDdbut, attributes)
    // this.attributeService.addClasses(htmlDdbut, attributes, ["btn"], ["btn-info"]) CHANGE TO STANDARD CHECKBOX CLASSES
    this.attributeService.addGeneralAttributes(htmlDdbut, attributes)

    this.cd.detectChanges()
  }
}
