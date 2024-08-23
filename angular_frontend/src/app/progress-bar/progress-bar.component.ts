import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from "@angular/core";
import { AttributeDto, ElementDto } from "../types/json-response.dto";
import { AttributeHelperService } from "../attribute-helper.service";

@Component({
	selector: 'app-progress-bar',
	templateUrl: './progress-bar.component.html',
	styleUrls: ['./progress-bar.component.scss']
})

export class ProgressBarComponent {
	@ViewChild('progress', { static: true }) progress!: ElementRef;
	@ViewChild('progressBar', { static: true }) progressBar!: ElementRef;
	@Input() element: ElementDto | null = null;

	@Input() parentLayout: string = "";

	value: number = 0;
	min: number = 0;
	max: number = 100;
	label: string = '';
	out_label: string = '';
	percentage: number = 0;

	constructor(private cd: ChangeDetectorRef, private attributeService: AttributeHelperService) { }

	ngAfterViewInit(): void {
		if (this.element != null) {
			this.setAttributes(this.element.attributes);

			this.cd.detectChanges();
		}
	}

	setAttributes(attributes: AttributeDto[]) {
		let valueAttr = this.attributeService.findAttribute("value", attributes);
		if (valueAttr != null) {
			this.value = Number(valueAttr.value);
		}
		let minAttr = this.attributeService.findAttribute("min", attributes);
		if (minAttr != null) {
			this.min = Number(minAttr.value);
		}
		let maxAttr = this.attributeService.findAttribute("max", attributes);
		if (maxAttr != null) {
			this.max = Number(maxAttr.value);
		}

		let labelAttr = this.attributeService.findAttribute("label", attributes);  // Handle label
		if (labelAttr != null) {
			this.label = labelAttr.value;
		}

		let out_labelAttr = this.attributeService.findAttribute("out_label", attributes);  // Handle out_label
		if (out_labelAttr != null) {
			this.out_label = out_labelAttr.value;
		}

		if (valueAttr != null) {
			this.percentage = this.value / (this.max - this.min) * 100;
		}

		let htmlProgressBar = this.progressBar.nativeElement;
		let htmlProgress = this.progress.nativeElement;

		this.attributeService.setAttributesDirectly(htmlProgress, attributes);
		this.attributeService.addAttributes(htmlProgress, attributes);
		// this.attributeService.addAttributes(htmlProgressBar, attributes);
		this.attributeService.addClasses(htmlProgressBar, attributes, ["progress-bar"], []);
	}
}


