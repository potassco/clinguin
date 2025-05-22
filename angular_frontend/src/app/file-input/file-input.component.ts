// file-input.component.ts
import { Component, ElementRef, Input, ViewChild, ChangeDetectorRef } from "@angular/core";
import { CallBackHelperService } from "../callback-helper.service";
import { AttributeDto, ElementDto, WhenDto } from "../types/json-response.dto";
import { ElementLookupService } from "../element-lookup.service";
import { ContextService } from "../context.service";
import { AttributeHelperService } from "../attribute-helper.service";

@Component({
  selector: "app-file-input",
  templateUrl: "./file-input.component.html"
})
export class FileInputComponent {
    @ViewChild('fileInput') fileInput!: ElementRef;
    @ViewChild('container') container!: ElementRef;
    @Input() element!: ElementDto;

    inputId = `file-input-${crypto.randomUUID()}`;
    acceptTypes = '.lp';
    isDisabled = false;

    constructor(
        private callBackHelper: CallBackHelperService,
        private elementLookupService: ElementLookupService,
        private contextService: ContextService,
        private attributeService: AttributeHelperService,
        private cd: ChangeDetectorRef
    ) {}

    ngAfterViewInit(): void {
        if (this.element) {
            this.setAttributes(this.element.attributes);
            this.elementLookupService.addElementObject(this.element.id, this, this.element);
            const htmlFileInput = this.fileInput.nativeElement;
            this.callBackHelper.setCallbacks(htmlFileInput, this.element.when);
        }
    }

    setAttributes(attributes: AttributeDto[]) {
        this.acceptTypes = this.attributeService.findGetAttributeValue("accept", attributes, '.lp');
        this.isDisabled = this.attributeService.findGetAttributeValue("disabled", attributes, 'false') === 'true';
        const htmlDdbut = this.container.nativeElement;
        this.attributeService.addClasses(htmlDdbut, attributes, ['form-group'], []);

        this.attributeService.addGeneralAttributes(this.fileInput.nativeElement, attributes);
        this.attributeService.setAttributesDirectly(this.fileInput.nativeElement, attributes);

        this.cd.detectChanges();
    }

    onFileSelected(event: any): void {
        const files = event.target.files;
        for (const file of files) {
            const reader = new FileReader();
            reader.onload = () => {
                const content = reader.result as string;
                const base64Content = btoa(unescape(encodeURIComponent(content)));
                
                this.contextService.addContext('_value', base64Content);
                
                const newWhen: WhenDto = {
                    id: this.element.id,
                    interactionType: 'call',
                    operation: `upload_file("${file.name}")`,
                    event: 'change',
                    actionType: ""
                };
                
                this.callBackHelper.handleCallback(newWhen, event);
            };
            reader.readAsText(file);
        }
    }
}