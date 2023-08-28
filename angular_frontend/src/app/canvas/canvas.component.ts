import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { ElementDto } from '../types/json-response.dto';
import { CallBackHelperService } from '../callback-helper.service';
import { AttributeHelperService } from '../attribute-helper.service';

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.scss']
})
export class CanvasComponent {
  @ViewChild("theImage",{static:false}) theImage! : ElementRef

  @Input() element: ElementDto | null = null

  imageSource: string = ""

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      console.log(window.location.href)

      let htmlDdbut = this.theImage.nativeElement

      this.attributeService.addAttributes(htmlDdbut, this.element.attributes)
      this.attributeService.textAttributes(htmlDdbut, this.element.attributes)
      this.attributeService.setAttributesDirectly(htmlDdbut, this.element.attributes)

      this.callbackService.setCallbacks(htmlDdbut, this.element.callbacks)

      let imgPath = this.attributeService.findAttribute("image_path", this.element.attributes)

      if (imgPath != null) {
        this.imageSource = imgPath.value
      }


      this.cd.detectChanges()
    }
  }


}
