import { ChangeDetectorRef, Component, Input, ElementRef, ViewChild } from '@angular/core';
import { AttributeDto, WhenDto, ElementDto } from '../types/json-response.dto';
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
  @ViewChild("titleIcon", { static: false }) titleIcon!: ElementRef

  public isCollapsed = true;

  title: string = ""
  // menuBarSections: MenuBarSection[] = []
  menuBarButtons: MenuBarButton[] = []

  constructor(private cd: ChangeDetectorRef, private displayFrontend: DrawFrontendService, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService, private callBackHelperService: CallBackHelperService) { }

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)
      this.element.children.forEach(menuBarButton => {
        let menuBarButtonTitle = this.attributeService.findGetAttributeValue("label", menuBarButton.attributes, "")
        let menuBarButtonOrder = this.attributeService.findGetAttributeValue("order", menuBarButton.attributes, "0")
        let menuBarButtonObject = new MenuBarButton(menuBarButton.id, menuBarButtonTitle, menuBarButton, menuBarButtonOrder)
        this.elementLookupService.addElementObject(menuBarButton.id, menuBarButtonObject, menuBarButton)
        this.menuBarButtons.push(menuBarButtonObject)
      })
      this.cd.detectChanges()

      this.menuBarButtons.sort((a: MenuBarButton, b: MenuBarButton) => {
        return a.order - b.order
      })

      this.menuBarButtons.forEach((menuBarButtonObject: MenuBarButton) => {
        let menuBarButtonHTML: HTMLElement | null = document.getElementById(menuBarButtonObject.id)
        if (menuBarButtonHTML != null) {
          menuBarButtonObject.setHtmlElement(menuBarButtonHTML)
          menuBarButtonObject.setAttributes(menuBarButtonObject.element.attributes)
          this.attributeService.addClasses(menuBarButtonHTML, menuBarButtonObject.element.attributes, ["btn-sm", "mx-1"], ["btn-outline-dark", "border-0"])

          this.callBackHelperService.setCallbacks(menuBarButtonHTML, menuBarButtonObject.element.when)

          let icon = menuBarButtonHTML.children.item(0)

          if (icon != null) {

            this.attributeService.addClasses(icon, menuBarButtonObject.element.attributes, ["fa"], [], 'icon')
          }
        }
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

    let iconHtml = this.titleIcon.nativeElement
    this.attributeService.addClasses(iconHtml, attributes, ["fa"], [], 'icon')


    this.cd.detectChanges()

  }

  operationExecutor(operation: WhenDto | null) {
    if (operation != null) {
      this.displayFrontend.operationPost(operation)
    }
  }
}

class MenuBarButton {
  id: string = ""
  title: string = ""
  element!: ElementDto
  order: number = 0
  htmlElement: HTMLElement | null = null

  constructor(id: string, title: string, element: ElementDto, order: string | null) {
    this.id = id
    this.title = title
    this.element = element
    this.order = order != null ? parseInt(order) : 0
  }

  setHtmlElement(htmlElement: HTMLElement) {
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

class MenuBarItem {
  id: string = ""
  title: string = ""
  element!: ElementDto
  htmlElement: HTMLElement | null = null

  constructor(id: string, title: string, element: ElementDto) {
    this.id = id
    this.title = title
    this.element = element
  }

  setHtmlElement(htmlElement: HTMLElement) {
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
  id: string = "menuBarSection"
  title: string = ""
  element!: ElementDto
  menuBarItems: MenuBarItem[] = []
  collapsed: boolean = true
  htmlElement: HTMLElement | null = null

  constructor(id: string, title: string, menuBarItems: MenuBarItem[], element: ElementDto) {
    this.id = id
    this.title = title
    this.menuBarItems = menuBarItems
    this.element = element
  }

  toggleCollapsed(): void {
    this.collapsed = !this.collapsed
  }

  setHtmlElement(htmlElement: HTMLElement) {
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
