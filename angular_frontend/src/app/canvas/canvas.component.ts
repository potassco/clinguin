import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { AttributeDto, WhenDto, ElementDto } from '../types/json-response.dto';
import { CallBackHelperService } from '../callback-helper.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { Buffer } from "buffer"; import { DATE_PIPE_DEFAULT_OPTIONS } from '@angular/common';
import { ElementLookupService } from '../element-lookup.service';
;

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.scss']
})
export class CanvasComponent {
  @ViewChild("theImage", { static: false }) theImage!: ElementRef
  @ViewChild("svgContainer", { static: false }) svgContainer!: ElementRef;

  @Input() element: ElementDto | null = null
  @Input() parentLayout: string = ""


  imageSource: string = ""

  imageType: string = ""


  constructor(private cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService) { }

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      let image = this.attributeService.findAttribute("image", this.element.attributes)
      let image_type = this.attributeService.findAttribute("image_type", this.element.attributes)

      if (image != null && image_type != null && image_type.value.startsWith("clingraph")) {
        this.svgImageHandler(this.element, image, image_type)
      } else {
        this.defaultImageHandler(this.element, image)
      }

      this.cd.detectChanges()
    }
  }

  setAttributes(attributes: AttributeDto[]) {
    console.log("TODO?")
  }

  svgImageHandler(element: ElementDto, image: AttributeDto, imageType: AttributeDto) {

    const decodeBase64 = (str: string): string => Buffer.from(str, 'base64').toString('binary');
    const regexPattern: RegExp = /\(([^,]+),\s*([^)]+)\)/;

    this.imageType = "svg"

    this.cd.detectChanges()

    // Add the SVG
    let svgString = decodeBase64(image.value)
    this.svgContainer.nativeElement.innerHTML = svgString

    this.cd.detectChanges()

    // Create necessary preprocessing lists
    let svgNodeElements = this.svgContainer.nativeElement.querySelectorAll(".node, .edge")
    // let svgEdgeElements = this.svgContainer.nativeElement.querySelectorAll(".edge")

    let nodeIdNodeElementLookup: { "key": string, "value": ElementDto }[] = []
    element.children.forEach(child => {
      let id_attr = this.attributeService.findAttribute("clingraph_id", child.attributes)

      if (id_attr != null) {
        let key = id_attr.value
        if (child.type == "svg_edge") {
          const match = key.match(regexPattern);
          if (!match) {
            console.error("Invalid edge format expected a tuple (X,Y) but got ", key)
          } else {
            key = match[1].replaceAll('"', '') + "--" + match[2].replaceAll('"', '')
            let key2 = match[1].replaceAll('"', '') + "-&gt;" + match[2].replaceAll('"', '')
            nodeIdNodeElementLookup.push({ "key": key2, "value": child })
          }
        }
        nodeIdNodeElementLookup.push({ "key": key, "value": child })
      }
    })

    let svgNodeUiNodeAssociationList = this.generateSvgNodeUiNodeAssociationList(svgNodeElements, nodeIdNodeElementLookup)

    this.addEventListeners(svgNodeUiNodeAssociationList)


    this.cd.detectChanges()
  }

  generateSvgNodeUiNodeAssociationList(svgNodeElements: any, nodeIdNodeElementLookup: { "key": string, "value": ElementDto }[]) {

    let svgNodeUiNodeAssociationList: { "svg": HTMLElement, "ui": ElementDto }[] = []

    svgNodeElements.forEach((svgNodeElement: HTMLElement) => {
      let correspondingElementDtoNode: null | ElementDto = null
      nodeIdNodeElementLookup.forEach((item: { "key": string, "value": ElementDto }) => {

        if (svgNodeElement.id == item.key) {
          correspondingElementDtoNode = item.value
        } else {
          for (const child of Array.from(svgNodeElement.children)) {
            if (child.tagName == "title") {
              if (child.innerHTML == item.key) {
                correspondingElementDtoNode = item.value
              }
            }
          }
        }
      })

      if (correspondingElementDtoNode != null) {
        this.elementLookupService.addElementTagHTML(correspondingElementDtoNode['id'], svgNodeElement, correspondingElementDtoNode)
        svgNodeUiNodeAssociationList.push({ "svg": svgNodeElement, "ui": correspondingElementDtoNode })

      } else {
        console.debug("Warning: No svgElement defined for clingraph element", svgNodeElement.id)
      }
    })

    return svgNodeUiNodeAssociationList
  }

  addEventListeners(svgNodeUiNodeAssociationList: { "svg": HTMLElement, "ui": ElementDto }[]) {

    svgNodeUiNodeAssociationList.forEach((elem: { "svg": HTMLElement, "ui": ElementDto }) => {
      let uiElement = elem.ui
      let clickRelatedDoList: WhenDto[] = []
      this.callbackService.setCallbacks(elem.svg, elem.ui.when)


    })
  }


  defaultImageHandler(element: ElementDto, image: AttributeDto | null) {
    this.imageType = "normal"

    this.cd.detectChanges()

    let htmlDdbut = this.theImage.nativeElement

    this.attributeService.addAttributes(htmlDdbut, element.attributes)
    this.callbackService.setCallbacks(htmlDdbut, element.when)

    let imgPath = this.attributeService.findAttribute("image_path", element.attributes)

    if (image != null) {
      this.imageSource = "data:image/png;base64," + image.value
    } else if (imgPath != null) {
      this.imageSource = imgPath.value
    }

  }


}
