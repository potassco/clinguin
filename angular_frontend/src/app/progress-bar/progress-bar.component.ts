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
	@Input() element: ElementDto | null = null;
	
	@Input() parentLayout: string = "";

	value: number = 0;
	label: string = '';

	constructor(private cd: ChangeDetectorRef, private attributeService: AttributeHelperService) {}

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

		let labelAttr = this.attributeService.findAttribute("label", attributes);  // Handle label
		if (labelAttr != null) {
		this.label = labelAttr.value;
		}		

		let htmlProgress = this.progress.nativeElement;
	
		this.attributeService.setAttributesDirectly(htmlProgress, attributes);
		this.attributeService.addAttributes(htmlProgress, attributes);
		this.attributeService.addClasses(htmlProgress, attributes, [], []);
	}
}
	
  
