import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild, ViewRef } from '@angular/core';
import { ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';

@Component({
  selector: 'app-label',
  templateUrl: './label.component.html',
  styleUrls: ['./label.component.scss']
})
export class LabelComponent {
  @ViewChild('label',{static:true}) label! : ElementRef
  @ViewChild('outerDiv',{static:true}) outerDiv! : ElementRef

  @Input() element: ElementDto | null = null

  elementLabel: string = ""

  constructor (private  cd: ChangeDetectorRef) {}


  ngAfterViewInit(): void {

    if (this.element != null) {
      let index = this.element.attributes.findIndex(attr => attr.key == "label")
      if (index >= 0) {
        console.log(this.element.attributes[index].value)
        this.elementLabel = this.element.attributes[index].value
      }

      let htmlDdbut = this.label.nativeElement
      let htmlOuterDiv = this.outerDiv.nativeElement

      AttributeHelperService.addAttributes(htmlDdbut, this.element.attributes)
      AttributeHelperService.textAttributes(htmlDdbut, this.element.attributes)
      AttributeHelperService.setAttributesDirectly(htmlDdbut, this.element.attributes)

      this.cd.detectChanges()
    }
  }
}

