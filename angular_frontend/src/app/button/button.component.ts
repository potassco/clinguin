import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss']
})
export class ButtonComponent {
  @ViewChild("theButton",{static:false}) theButton! : ElementRef

  @Input() element: ElementDto | null = null

  buttonLabel: string = ""

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      let index = this.element.attributes.findIndex(attr => attr.key == "label")
      if (index >= 0) {
        this.buttonLabel = this.element.attributes[index].value
      }

      let htmlDdbut = this.theButton.nativeElement

      this.attributeService.addAttributes(htmlDdbut, this.element.attributes)
      this.attributeService.textAttributes(htmlDdbut, this.element.attributes)
      this.attributeService.setAttributesDirectly(htmlDdbut, this.element.attributes)

      this.callbackService.setCallbacks(htmlDdbut, this.element.callbacks)

      this.cd.detectChanges()
    }
  }
}
