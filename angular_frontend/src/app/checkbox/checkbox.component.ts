import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { AttributeDto, ElementDto } from "../types/json-response.dto";
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { CallBackHelperService } from "../callback-helper.service";

@Component({
    selector: 'app-checkbox',
    templateUrl: './checkbox.component.html',
    styleUrls: ['./checkbox.component.scss']
})
export class CheckboxComponent {
    @ViewChild('checkbox', { static: false }) checkbox!: ElementRef
    @ViewChild('checkboxForm', { static: false }) checkboxForm!: ElementRef

    @Input() element: ElementDto | null = null
    @Input() parentLayout: string = ""

    checkboxID: string = crypto.randomUUID();
    checkboxLabel: string = ""
    disabledAttribute: boolean = false
    checked: boolean = false
    type: string = "checkbox"

    constructor(private cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService) { }

    ngAfterViewInit(): void {
        if (this.element != null) {
            this.elementLookupService.addElementObject(this.element.id, this, this.element)

            this.setAttributes(this.element.attributes)
            let htmlDdbut = this.checkbox.nativeElement
            this.callbackService.setCallbacks(htmlDdbut, this.element.when)

            this.cd.detectChanges()
        }
    }

    setAttributes(attributes: AttributeDto[]) {
        this.checkboxLabel = this.attributeService.findGetAttributeValue("label", attributes, "")
        let valueAttr = this.attributeService.findAttribute("checked", attributes);
        if (valueAttr != null) {
            this.checked = true;
        }

        let typeAttr = this.attributeService.findAttribute("type", attributes);
        if (typeAttr != null) {
            if (typeAttr.value === "checkbox" || typeAttr.value === "radio") {
                this.type = typeAttr.value;
            } else {
                console.warn("Invalid value for type attribute. Defaulting to checkbox.");
                this.type = "checkbox";
            }
        }

        let htmlDdbut = this.checkbox.nativeElement
        let htmlFormDdbut = this.checkboxForm.nativeElement

        this.attributeService.setAttributesDirectly(htmlDdbut, attributes)
        this.attributeService.addAttributes(htmlDdbut, attributes)
        this.attributeService.textAttributes(htmlDdbut, attributes)
        this.attributeService.addClasses(htmlFormDdbut, attributes, [], [])
        this.attributeService.addGeneralAttributes(htmlDdbut, attributes)

        let stringDisabled = this.attributeService.findGetAttributeValue("disabled", attributes, "false")
        if (stringDisabled == "false") {
            this.disabledAttribute = false
        } else if (stringDisabled == "true") {
            this.disabledAttribute = true
        } else {
            console.warn("NOT SUPPORTED VALUE FOR DISABLED (assuming not disabled): ")
            console.log(stringDisabled)
            this.disabledAttribute = false
        }

        this.cd.detectChanges()
    }
}