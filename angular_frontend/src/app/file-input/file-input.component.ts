import { Component, ElementRef, Input, ViewChild } from "@angular/core";
import { AttributeDto, ElementDto, WhenDto } from "../types/json-response.dto";
import { ElementLookupService } from "../element-lookup.service";
import { ContextService } from "../context.service";
import { AttributeHelperService } from "../attribute-helper.service";
import { DrawFrontendService } from "../draw-frontend.service";
import { CallBackHelperService } from '../callback-helper.service';

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
        private frontendService: DrawFrontendService,
        private callbackHelperService: CallBackHelperService
    ) { }

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
        console.log('Uploading file:', files[index]?.name, 'Index:', index);
        if (index >= files.length) return;
        const file = files[index];
        const reader = new FileReader();
        reader.onload = () => {
            this.contextService.addContext('filename', file.name);
            this.contextService.addContext('filecontent', btoa(reader.result as string));

            const changeCallbacks = this.element.when?.filter(when => when.event === 'change') || [];
            console.log('Change callbacks for file input:', changeCallbacks);

            for (const changeCallback of changeCallbacks) {
                console.log('Processing change callback for file input:', changeCallback);
                if (!changeCallback) {
                    this.frontendService.postMessage(
                        'No action found for file input change',
                        'warning'
                    );
                } else {

                    if (changeCallback.interactionType === 'call') {
                        const changeCallbackCopy = { ...changeCallback };
                        console.log('Executing change callback for file input:', changeCallbackCopy);
                        this.callbackHelperService.handleCallback(changeCallbackCopy, null)

                    } else if (changeCallback.interactionType === 'update') {
                        console.log('Updating modal visibility for file input:', changeCallback);
                        this.callbackHelperService.handleUpdate(changeCallback, null);
                    }
                }


                setTimeout(() => this.uploadFiles(files, index + 1), 100);
            }

        };
        reader.readAsText(file);
    }


}
