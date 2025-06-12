import { Component, ElementRef, Input, ViewChild } from "@angular/core";
import { AttributeDto, ElementDto, WhenDto } from "../types/json-response.dto";
import { ElementLookupService } from "../element-lookup.service";
import { ContextService } from "../context.service";
import { AttributeHelperService } from "../attribute-helper.service";
import { DrawFrontendService } from "../draw-frontend.service";

@Component({
  selector: "app-file-input",
  templateUrl: "./file-input.component.html"
})
export class FileInputComponent {
    @ViewChild('fileInput') fileInput!: ElementRef;
    @ViewChild('container') container!: ElementRef;
    @Input() element!: ElementDto;

    constructor(
        private elementLookupService: ElementLookupService,
        private contextService: ContextService,
        private attributeService: AttributeHelperService,
        private frontendService: DrawFrontendService
    ) {}

    ngAfterViewInit(): void {
        this.setAttributes(this.element.attributes);
        this.elementLookupService.addElementObject(this.element.id, this, this.element);
    }

    setAttributes(attributes: AttributeDto[]) {
        const accept = this.attributeService.findGetAttributeValue("accept", attributes, '.lp');
        const disabled = this.attributeService.findGetAttributeValue("disabled", attributes, 'false') === 'true';
        const multiple = this.attributeService.findGetAttributeValue("multiple", attributes, 'false') === 'true';
        
        this.fileInput.nativeElement.accept = accept;
        this.fileInput.nativeElement.disabled = disabled;
        this.fileInput.nativeElement.multiple = multiple;
        
        this.attributeService.addClasses(this.container.nativeElement, attributes, ['form-group'], []);
        this.attributeService.addGeneralAttributes(this.fileInput.nativeElement, attributes);
    }

    onFileSelected(event: any): void {
        const files = Array.from(event.target.files) as File[];
        if (!files || files.length === 0) return;
        
        this.uploadFiles(files, 0);
    }

    private uploadFiles(files: File[], index: number): void {
		if (index >= files.length) return;
		const file = files[index];
		const reader = new FileReader();
		reader.onload = () => {
			this.contextService.addContext('_value', btoa(reader.result as string));
			const changeCallback = this.element.when?.find(w =>
			w.actionType === 'change' && w.interactionType === 'call'
			);
			if (changeCallback) {
			changeCallback.operation =
				`upload_file("${file.name}")`;
			this.frontendService.operationPost(changeCallback);
			}
			setTimeout(() => this.uploadFiles(files, index + 1), 100);
		};
		reader.readAsText(file);
		}
}
