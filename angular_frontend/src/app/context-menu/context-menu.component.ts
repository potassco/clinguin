import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';

@Component({
  selector: 'app-context-menu',
  templateUrl: './context-menu.component.html',
  styleUrls: ['./context-menu.component.scss']
})
export class ContextMenuComponent {

  @Input() element: ElementDto | null = null

  menuId:string = ""
  buttonList: {id:string,text:string,attributes:AttributeDto[]}[] = []

  constructor (private  cd: ChangeDetectorRef, private attributeService: AttributeHelperService, private callbackService: CallBackHelperService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {

      this.menuId = "menu-" + this.element.id

      this.element.children.forEach((item:ElementDto) => {
        let id = item.id

        let text = this.attributeService.findGetAttributeValue("label", item.attributes, "")

        this.buttonList.push({id:id, text:text, attributes: item.attributes})
      })

      this.cd.detectChanges()

      this.element.children.forEach((item:ElementDto) => {
        let button = document.getElementById(item.id)
        if (button != null) {
          this.callbackService.setCallbacks(button, item.when)
        }
      })
      
      this.cd.detectChanges()

      this.buttonList.forEach((listButton:{id:string,text:string,attributes:AttributeDto[]}) => {
        let listButtonHTML : HTMLElement | null = document.getElementById(listButton.id)
        if (listButtonHTML != null) {
          this.attributeService.addClasses(listButtonHTML, listButton.attributes, ["list-group-item", "list-group-item-action"],[])

          let link = listButtonHTML.children.item(0)
          console.log(link)
          if (link!= null){

            let icon = link.children.item(0)
  
            if (icon != null) {
        
              this.attributeService.addClasses(icon, listButton.attributes, ["fa"], [], 'icon')
            }
          }
        }
      })

    }
  }

}
