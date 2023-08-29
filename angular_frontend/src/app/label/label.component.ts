import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild, ViewRef } from '@angular/core';
import { ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';

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

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService) {}


  ngAfterViewInit(): void {

    if (this.element != null) {
      let index = this.element.attributes.findIndex(attr => attr.key == "label")
      if (index >= 0) {
        this.elementLabel = this.element.attributes[index].value
      }

      let htmlDdbut = this.label.nativeElement
      let htmlMiddle = this.middleDiv.nativeElement
      let htmlOuterDiv = this.outerDiv.nativeElement

      this.attributeService.addAttributes(htmlDdbut, this.element.attributes)
      this.attributeService.textAttributes(htmlDdbut, this.element.attributes)
      this.attributeService.setAttributesDirectly(htmlDdbut, this.element.attributes)

      this.callbackService.setCallbacks(htmlDdbut, this.element.callbacks)

      this.setOuterDivStyles(htmlOuterDiv)
      this.setMiddleDivStyle(htmlMiddle)
      this.setParagraphStyle(htmlDdbut)

      this.cd.detectChanges()
    }
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

