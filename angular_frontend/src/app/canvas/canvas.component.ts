import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { AttributeDto, DoDto, ElementDto } from '../types/json-response.dto';
import { CallBackHelperService } from '../callback-helper.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { Buffer } from "buffer";import { DATE_PIPE_DEFAULT_OPTIONS } from '@angular/common';
;

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.scss']
})
export class CanvasComponent {
  @ViewChild("theImage",{static:false}) theImage! : ElementRef
  @ViewChild("svgContainer",{static:false}) svgContainer!:ElementRef;

  @Input() element: ElementDto | null = null
  @Input() parentLayout: string = ""


  imageSource: string = ""

  imageType: string = ""


  constructor (private  cd: ChangeDetectorRef, private callbackService: CallBackHelperService, private attributeService: AttributeHelperService) {}

  ngAfterViewInit(): void {

    if (this.element != null) {
      console.log(this.element)
      
      let image = this.attributeService.findAttribute("image", this.element.attributes)
      let image_type = this.attributeService.findAttribute("image_type", this.element.attributes)

      if (image != null && image_type != null && image_type.value == "clingraph_svg") {
        this.svgImageHandler(this.element, image, image_type) 
      } else {
        this.defaultImageHandler(this.element, image)
      }

      this.cd.detectChanges()
    }
  }

  svgImageHandler(element: ElementDto, image: AttributeDto, iamgeType : AttributeDto) {
    
    const decodeBase64 = (str: string):string => Buffer.from(str, 'base64').toString('binary');

    this.imageType = "svg"

    this.cd.detectChanges()
   
    // Add the SVG
    let svgString = decodeBase64(image.value)
    this.svgContainer.nativeElement.innerHTML = svgString 

    this.cd.detectChanges()

    // Create necessary preprocessing lists
    let svgNodeElements = this.svgContainer.nativeElement.querySelectorAll(".node")

    let nodeIdNodeElementLookup : {"key":string, "value":ElementDto}[] = []
    element.children.forEach(child => {
      let id_attr = this.attributeService.findAttribute("id", child.attributes)

      if (id_attr != null) {
        let key = id_attr.value
        nodeIdNodeElementLookup.push({"key":key,"value":child})
      }
    })

    let svgNodeUiNodeAssociationList = this.generateSvgNodeUiNodeAssociationList(svgNodeElements, nodeIdNodeElementLookup)

    this.addEventListeners(svgNodeUiNodeAssociationList)

    
    this.cd.detectChanges()
  }

  generateSvgNodeUiNodeAssociationList(svgNodeElements : any, nodeIdNodeElementLookup : {"key":string, "value":ElementDto}[]) {
    
    let svgNodeUiNodeAssociationList : {"svg":HTMLElement, "ui":ElementDto}[] = []

    svgNodeElements.forEach((svgNodeElement : HTMLElement) => {
      let correspondingElementDtoNode : null | ElementDto = null

      nodeIdNodeElementLookup.forEach((item:{"key":string,"value":ElementDto}) => {
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
        svgNodeUiNodeAssociationList.push({"svg":svgNodeElement,"ui":correspondingElementDtoNode})

      } else {
        console.log("Warning: Could not find for the following svgNodeElement a corresponding ui.lp node!")
        console.log(svgNodeElement)
      }
    })

    return svgNodeUiNodeAssociationList
  }

  addEventListeners(svgNodeUiNodeAssociationList : {"svg":HTMLElement, "ui":ElementDto}[]) {
    
    svgNodeUiNodeAssociationList.forEach((elem : {"svg":HTMLElement, "ui":ElementDto}) => {
      let uiElement = elem.ui
      let clickRelatedDoList : DoDto[] = []

      uiElement.do.forEach((do_: DoDto) => {
        if (do_.actionType == "click") {
          clickRelatedDoList.push(do_)
        }
      })

      elem.svg.addEventListener("click",function(){
        clickRelatedDoList.forEach((do_:DoDto) => {
          if (do_.interactionType == "update") {
            let policy = do_.policy

            policy = policy.substring(1)
            policy = policy.slice(0,-1)
            let splits = policy.split(",")

            let id = splits[0]
            let key = splits[1]
            let value = splits[2]

            let searchedElement : null | HTMLElement = document.getElementById(id)
            if (searchedElement != null) {
              if (key == "visibility") {
                if (value == "hidden") {
                  searchedElement.style.visibility = "hidden"
                } else if (value == "shown") {
                  searchedElement.style.visibility = "visible"
                }
              }
            }
          }
        })
      })
    })
  }


  defaultImageHandler(element : ElementDto, image : AttributeDto | null) {
    this.imageType = "normal"
    
    this.cd.detectChanges()
        
    let htmlDdbut = this.theImage.nativeElement

    this.attributeService.addAttributes(htmlDdbut, element.attributes)
    this.attributeService.textAttributes(htmlDdbut, element.attributes)
    this.attributeService.setAttributesDirectly(htmlDdbut, element.attributes)

    this.callbackService.setCallbacks(htmlDdbut, element.do)

    let imgPath = this.attributeService.findAttribute("image_path", element.attributes)

    if (image != null) {
      this.imageSource ="data:image/png;base64," + image.value
    } else if (imgPath != null) {
      this.imageSource = imgPath.value
    }

  }


}
