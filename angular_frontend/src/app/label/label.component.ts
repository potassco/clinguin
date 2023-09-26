import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild, ViewRef } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';
import { ElementLookupService } from '../element-lookup.service';

@Component({
  selector: 'app-label',
  templateUrl: './label.component.html',
  styleUrls: ['./label.component.scss']
})
export class LabelComponent {
  @ViewChild('label',{static:true}) label! : ElementRef
  @ViewChild('middleDiv', {static:true}) middleDiv!: ElementRef
  @ViewChild('outerDiv',{static:true}) outerDiv! : ElementRef

  @Input() element: ElementDto | null = null
  @Input() parentLayout: string = ""

  elementLabel: string = ""

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService) {}


  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      let htmlDdbut = this.label.nativeElement

      this.callbackService.setCallbacks(htmlDdbut, this.element.when)

      this.setAttributes(this.element.attributes)
      
      this.cd.detectChanges()   
    }
  }

  setAttributes(attributes: AttributeDto[]) {
      let label = this.attributeService.findAttribute("label", attributes)
      if (label != null) {
        this.elementLabel = label.value
      }

      let htmlDdbut = this.label.nativeElement
      let htmlMiddle = this.middleDiv.nativeElement
      let htmlOuterDiv = this.outerDiv.nativeElement

      this.attributeService.addAttributes(htmlDdbut, attributes)
      this.attributeService.textAttributes(htmlDdbut, attributes)
      this.attributeService.setAttributesDirectly(htmlDdbut, attributes)
      this.attributeService.addClasses(htmlDdbut, attributes, [],[])


      this.setOuterDivStyles(htmlOuterDiv)
      this.setMiddleDivStyle(htmlMiddle)
      this.setParagraphStyle(htmlDdbut)

      this.cd.detectChanges()   
  }

  setOuterDivStyles(outerDiv:HTMLElement) {
    outerDiv.style.display = "table"
    outerDiv.style.minHeight = "100%"
    outerDiv.style.minWidth = "100%"
    outerDiv.style.overflow = "hidden"
  }

  setMiddleDivStyle(middleDiv:HTMLElement) {
    middleDiv.style.minWidth = "100%"
    middleDiv.style.display = "table-row"
    //style="display:table-row; min-width: 100%;"
  }

  setParagraphStyle(paragraph:HTMLElement) {

    paragraph.style.display = "table-cell"
    paragraph.style.verticalAlign = "middle"
    paragraph.style.textAlign = "center"
  }
}

