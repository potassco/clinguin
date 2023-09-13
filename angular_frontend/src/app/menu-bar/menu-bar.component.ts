import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { AttributeDto, DoDto, ElementDto } from '../types/json-response.dto';
import { DrawFrontendService } from '../draw-frontend.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';
import { ElementLookupService } from '../element-lookup.service';

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

  constructor(private cd: ChangeDetectorRef, private displayFrontend: DrawFrontendService, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.element.children.forEach(child => {
        let menuBarItems: MenuBarItem[] = []

        child.children.forEach(child => {

          let menuBarItemTitle = this.attributeService.findGetAttributeValue("label", child.attributes, "")
          let callback = this.callbackService.findCallback("click", child.do)

          let menuBarItem = new MenuBarItem(child.id, menuBarItemTitle, callback)
          this.elementLookupService.addElementObject(child.id, menuBarItem, child)
          menuBarItems.push(menuBarItem)
        
        })

        let menuBarTitle = this.attributeService.findGetAttributeValue("label", child.attributes, "")
        let menuBarSectionId = child.id

        let menuBarSection = new MenuBarSection(menuBarSectionId, menuBarTitle, menuBarItems)
        this.elementLookupService.addElementObject(child.id, menuBarSection, child)
        this.menuBarSections.push(menuBarSection)
      })

    this.setAttributes(this.element.attributes)

    this.cd.detectChanges()
    }
  }
  
  setAttributes(attributes: AttributeDto[]) {
    let title = this.attributeService.findAttribute("title", attributes)
    if (title != null) {
      this.title = title.value
    }

    this.cd.detectChanges()

  }

  policyExecutor(policy: DoDto | null) {
    if (policy != null) {
      this.displayFrontend.policyPost(policy)
    }
  }
}

class MenuBarItem {
  id:string=""
  title:string=""
  policy!:DoDto | null

  constructor(id:string, title: string, policy:DoDto | null) {
    this.id = id
    this.title = title
    this.policy = policy
  }

  setAttributes(attributes: AttributeDto[]) {
    let title = attributes.find((item: AttributeDto) => item.key == "label")
    if (title != null) {
      this.title = title.value
    } else {
      this.title = ""
    }
  }
}

class MenuBarSection {
  id : string = "menuBarSection"
  title:string = ""
  menuBarItems:MenuBarItem[] = []
  collapsed:boolean = true

  constructor(id: string, title:string, menuBarItems:MenuBarItem[]) {
    this.id = id
    this.title = title
    this.menuBarItems = menuBarItems
  }

  toggleCollapsed() : void {
    this.collapsed = !this.collapsed 
  }

  setAttributes(attributes: AttributeDto[]) {
    let title = attributes.find((item: AttributeDto) => item.key == "label")
    if (title != null) {
      this.title = title.value
    } else {
      this.title = ""
    }
  }
  
}
