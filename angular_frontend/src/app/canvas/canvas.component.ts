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

  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      console.log(window.location.href)

      let htmlDdbut = this.theImage.nativeElement

      AttributeHelperService.addAttributes(htmlDdbut, this.element.attributes)
      AttributeHelperService.textAttributes(htmlDdbut, this.element.attributes)
      AttributeHelperService.setAttributesDirectly(htmlDdbut, this.element.attributes)

      this.callbackService.setCallbacks(htmlDdbut, this.element.callbacks)

      let imgPath = AttributeHelperService.findAttribute("image_path", this.element.attributes)

      if (imgPath != null) {
        this.imageSource = imgPath.value
      }


      this.cd.detectChanges()
    }
  }


}
