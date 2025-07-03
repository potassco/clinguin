import { ChangeDetectorRef, Component, Input, AfterViewInit, ElementRef, ViewChild, Inject, OnInit } from '@angular/core';
import { DOCUMENT } from "@angular/common";
import 'leader-line';
declare let LeaderLine: any;
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { DrawFrontendService } from '../draw-frontend.service';
import { animation } from '@angular/animations';

@Component({
  selector: 'app-line',
  templateUrl: './line.component.html',
  styleUrls: ['./line.component.scss']
})
export class LineComponent implements AfterViewInit {

  @ViewChild('lineContainer', { static: false }) lineContainer!: ElementRef;
  @Input() element: ElementDto | null = null

  start: string = "";
  end: string = "";

  options: { [key: string]: any } = {
    color: "#0052CC",
    size: 2,
    path: "arc",
    startSocket: "",
    endSocket: "",
    startSocketGravity: 0,
    endSocketGravity: 0,
    startPlug: "",
    endPlug: "",
    startPlugColor: "",
    endPlugColor: "",
    startPlugSize: 2,
    endPlugSize: 2,
    outline: false,
    outlineColor: "",
    outlineSize: 1,
    startPlugOutline: false,
    endPlugOutline: false,
    startPlugOutlineSize: 1,
    endPlugOutlineSize: 1,
    startPlugOutlineColor: "",
    endPlugOutlineColor: "",
    startLabel: "",
    endLabel: "",
    middleLabel: "",
    dash: false,
    gradient: false,
    dropShadow: false,

  }

  line!: any;

  constructor(private cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService, private drawFrontendService: DrawFrontendService) { }

  ngAfterViewInit(): void {
    // Delay to ensure DOM is fully rendered
    if (this.element != null) {
      this.setAttributes(this.element.attributes)
    }

    setTimeout(() => {
      const elementByIdStart = document.getElementById(this.start);
      const elementByIdEnd = document.getElementById(this.end);

      if (elementByIdStart && elementByIdEnd && elementByIdEnd !== elementByIdStart) {
        this.line = new LeaderLine(elementByIdStart, elementByIdEnd, this.options);
        this.drawFrontendService.lines.push(this.line);
      }
      else {
        console.warn('One or both elements not found! Or both are the same');
      }
    }, 10);
  }

  setAttributes(attributes: AttributeDto[]) {
    this.start = this.attributeService.findGetAttributeValue("start", attributes, "")
    this.end = this.attributeService.findGetAttributeValue("end", attributes, "")
    attributes.forEach((attr: AttributeDto) => {
      this.options[attr.key] = attr.value
    })
  }
}

