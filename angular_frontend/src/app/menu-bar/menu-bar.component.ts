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

  constructor(private cd: ChangeDetectorRef, private displayFrontend: DrawFrontendService, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService, private callBackHelperService:CallBackHelperService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.element.children.forEach(menuBarSection => {
        let menuBarItems: MenuBarItem[] = []

        menuBarSection.children.forEach(menuBarSectionItem => {

          let menuBarItemTitle = this.attributeService.findGetAttributeValue("label", menuBarSectionItem.attributes, "")

          let menuBarItemObject = new MenuBarItem(menuBarSectionItem.id, menuBarItemTitle, menuBarSectionItem)
          this.elementLookupService.addElementObject(menuBarSectionItem.id, menuBarItemObject, menuBarSectionItem)
          menuBarItems.push(menuBarItemObject)
        
        })

        let menuBarTitle = this.attributeService.findGetAttributeValue("label", menuBarSection.attributes, "")
        let menuBarSectionId = menuBarSection.id

        let menuBarSectionObject = new MenuBarSection(menuBarSectionId, menuBarTitle, menuBarItems, menuBarSection)
        this.elementLookupService.addElementObject(menuBarSection.id, menuBarSectionObject, menuBarSection)
        this.menuBarSections.push(menuBarSectionObject)

        this.cd.detectChanges()

        let htmlChild : HTMLElement | null = document.getElementById(menuBarSection.id)
        if (htmlChild != null) {
          menuBarSectionObject.setHtmlElement(htmlChild)
          menuBarSectionObject.setAttributes(menuBarSection.attributes)

          this.callBackHelperService.setCallbacks(htmlChild, menuBarSection.do)
        }
      
        menuBarSectionObject.menuBarItems.forEach((menuBarSectionItemObject:MenuBarItem) => {
   
          let menuBarSectionItemHTML : HTMLElement | null = document.getElementById(menuBarSectionItemObject.id)
          if (menuBarSectionItemHTML != null) {
            menuBarSectionItemObject.setHtmlElement(menuBarSectionItemHTML)
            menuBarSectionItemObject.setAttributes(menuBarSectionItemObject.element.attributes)
          
            this.callBackHelperService.setCallbacks(menuBarSectionItemHTML, menuBarSectionItemObject.element.do)
          }
        })
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
  element!:ElementDto
  htmlElement:HTMLElement| null = null

  constructor(id:string, title: string, element: ElementDto) {
    this.id = id
    this.title = title
    this.element = element
  }

  setHtmlElement(htmlElement:HTMLElement) {
    this.htmlElement = htmlElement
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
  element!:ElementDto
  menuBarItems:MenuBarItem[] = []
  collapsed:boolean = true
  htmlElement:HTMLElement| null = null

  constructor(id: string, title:string, menuBarItems:MenuBarItem[], element: ElementDto) {
    this.id = id
    this.title = title
    this.menuBarItems = menuBarItems
    this.element = element
  }

  toggleCollapsed() : void {
    this.collapsed = !this.collapsed 
  }

  setHtmlElement(htmlElement:HTMLElement) {
    this.htmlElement = htmlElement
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
