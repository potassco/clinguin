import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { CallbackDto, ElementDto } from '../types/json-response.dto';
import { DrawFrontendService } from '../draw-frontend.service';

@Component({
  selector: 'app-menu-bar',
  templateUrl: './menu-bar.component.html',
  styleUrls: ['./menu-bar.component.scss']
})
export class MenuBarComponent {
  @Input() element: ElementDto | null = null

  public isCollapsed = true;
  public isCollapsed2 = true;

  title: string = ""
  menuBarSections: MenuBarSection[] = []

  constructor(private cd: ChangeDetectorRef, private displayFrontend: DrawFrontendService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      console.log(this.element)

      let index = this.element.attributes.findIndex(attr => attr.key == "title")
      if (index >= 0) {
        this.title = this.element.attributes[index].value
      }


      this.element.children.forEach(child => {
        let menuBarItems: MenuBarItem[] = []

        child.children.forEach(child => {

          let title = ""
          let index = child.attributes.findIndex(attr => attr.key == "label")
          if (index >= 0) {
            title = child.attributes[index].value
          }

          let policy = null
          index = child.callbacks.findIndex(callback => callback.action == "click")
          if (index >= 0) {
            policy = child.callbacks[index]
            let menuBarItem = new MenuBarItem(title, policy)
            menuBarItems.push(menuBarItem)
          }

        })

        let title = ""
        let index = child.attributes.findIndex(attr => attr.key == "label")
        if (index >= 0) {
          title = child.attributes[index].value
        }

        let menuBarSection = new MenuBarSection(title, menuBarItems)
        this.menuBarSections.push(menuBarSection)
      })
    this.cd.detectChanges()
    }
  }

  policyExecutor(policy: CallbackDto) {
    console.log(policy)
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

  constructor(title:string, menuBarItems:MenuBarItem[]) {
    this.title = title
    this.menuBarItems = menuBarItems
  }
}
