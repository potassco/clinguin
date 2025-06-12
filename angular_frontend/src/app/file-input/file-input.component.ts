import { Component, ElementRef, Input, ViewChild } from "@angular/core";
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
	@Input() element!: ElementDto;

	acceptTypes = '.lp';
	isDisabled = false;

	constructor(
		private callBackHelper: CallBackHelperService,
		private elementLookupService: ElementLookupService,
		private contextService: ContextService,
		private attributeService: AttributeHelperService
	) {}

	ngAfterViewInit(): void {
		if (this.element) {
			this.setAttributes(this.element.attributes);
			this.elementLookupService.addElementObject(this.element.id, this, this.element);
		}
	}

	setAttributes(attributes: AttributeDto[]) {
		this.acceptTypes = this.attributeService.findGetAttributeValue("accept", attributes, '.lp');
		this.isDisabled = this.attributeService.findGetAttributeValue("disabled", attributes, 'false') === 'true';
		
		const input = this.fileInput.nativeElement;
		this.attributeService.addGeneralAttributes(input, attributes);
		this.attributeService.setAttributesDirectly(input, attributes);
	}

	onFileSelected(event: any): void {
		const files = Array.from(event.target.files || []) as File[];
		this.uploadFilesSequentially(files, event, 0);
		event.target.value = '';
	}

	private uploadFilesSequentially(files: File[], event: Event, index: number): void {
		if (index >= files.length) return;
		
		const file = files[index];
		const reader = new FileReader();
		reader.onload = () => {
			const base64Content = btoa(unescape(encodeURIComponent(reader.result as string)));
			
			this.contextService.clearContext();
			this.contextService.addContext('_value', base64Content);
			
			const operation: WhenDto = {
				id: this.element.id,
				interactionType: 'call',
				operation: `upload_file("${file.name}")`,
				event: 'change',
				actionType: 'call'
			};
			
			this.callBackHelper.handleCallback(operation, event);
			
			setTimeout(() => {
				this.uploadFilesSequentially(files, event, index + 1);
			}, 500);
		};
		reader.readAsText(file);
	}
}