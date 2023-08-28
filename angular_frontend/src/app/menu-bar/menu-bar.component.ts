import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { CallbackDto, ElementDto } from '../types/json-response.dto';
import { DrawFrontendService } from '../draw-frontend.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';

@Component({
  selector: 'app-menu-bar',
  templateUrl: './menu-bar.component.html',
  styleUrls: ['./menu-bar.component.scss']
})
export class MenuBarComponent {
  @Input() element: ElementDto | null = null

  public isCollapsed = true;

  title: string = ""
  menuBarSections: MenuBarSection[] = []

  constructor(private cd: ChangeDetectorRef, private displayFrontend: DrawFrontendService, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {

      let index = this.element.attributes.findIndex(attr => attr.key == "title")
      if (index >= 0) {
        this.title = this.element.attributes[index].value
      }

      this.element.children.forEach(child => {
        let menuBarItems: MenuBarItem[] = []

        child.children.forEach(child => {

          let title = this.attributeService.findGetAttributeValue("label", child.attributes, "")

          let callback = this.callbackService.findCallback("click", child.callbacks)
          if (callback != null) {
            let menuBarItem = new MenuBarItem(title, callback)
            menuBarItems.push(menuBarItem)
          }

        })

        let menuBarTitle = this.attributeService.findGetAttributeValue("label", child.attributes, "")

        let menuBarSection = new MenuBarSection(menuBarTitle, menuBarItems)
        this.menuBarSections.push(menuBarSection)
      })
    this.cd.detectChanges()
    }
  }

  policyExecutor(policy: CallbackDto) {
    this.displayFrontend.policyPost(policy)
  }
}

class MenuBarItem {
  title:string=""
  policy!:CallbackDto

  constructor(title: string, policy:CallbackDto) {
    this.title = title
    this.policy = policy
  }
}

class MenuBarSection {
  title:string = ""
  menuBarItems:MenuBarItem[] = []
  collapsed:boolean = true

  constructor(title:string, menuBarItems:MenuBarItem[]) {
    this.title = title
    this.menuBarItems = menuBarItems
  }

  toggleCollapsed() : void {
    this.collapsed = !this.collapsed 
  }
}
