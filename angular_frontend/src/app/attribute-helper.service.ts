import { Attribute, Injectable } from '@angular/core';
import { AttributeDto, ElementDto } from './types/json-response.dto';

@Injectable({
  providedIn: 'root'
})
export class AttributeHelperService {

  constructor() { }


    static attrBackgroundColor(html:HTMLElement, attribute: AttributeDto) {
        let value = attribute.value


        html.style.backgroundColor = value
    }

    static attrHeight(html:HTMLElement, attribute: AttributeDto) {
        let value = attribute.value + "px"
        html.style.height = value
    }

    static attrWidth(html:HTMLElement, attribute: AttributeDto) {
        let value = attribute.value + "px"
        html.style.width = value
    }


    static setBorderHelper(html:HTMLElement, attributes: AttributeDto[]) {

        let borderWidth = Number(AttributeHelperService.findGetAttributeValue("border_width", attributes, "0"))
        let borderColor = AttributeHelperService.findGetAttributeValue("border_color",attributes, "black")
        let borderStyle = "solid"

        AttributeHelperService.setBorder(html, borderWidth, borderColor, borderStyle)
    }

    static setBorder(html:HTMLElement, borderWidth: number, borderColor: string, borderStyle: string) {
        if (borderWidth > 0) {
            html.style.border = String(borderWidth) + "px " + borderStyle + " " + borderColor
        }

    }

    static addAttributes(html:HTMLElement, attributes : AttributeDto[]) {

        let attr_dict = [
            {key:"background_color",value:AttributeHelperService.attrBackgroundColor},
            {key:"height", value:AttributeHelperService.attrHeight},
            {key:"width", value:AttributeHelperService.attrWidth},
        ]

        attributes.forEach(attribute => {
            let index = attr_dict.findIndex(item => item.key == attribute.key)
            if (index >= 0) {
                attr_dict[index].value(html,attribute)
            }
        })

        AttributeHelperService.setGrid(html,attributes)
        AttributeHelperService.setBorderHelper(html, attributes)
        AttributeHelperService.setHover(html, attributes)
        AttributeHelperService.setChildLayout(html, attributes)
    }

    static setGrid(html: HTMLElement, attributes:AttributeDto[]) {

        let gridRowStart = AttributeHelperService.findAttribute("grid_row", attributes)
        let gridRowSpan = AttributeHelperService.findAttribute("grid_row_span", attributes)
        let gridColumnStart = AttributeHelperService.findAttribute("grid_column", attributes)
        let gridColumnSpan = AttributeHelperService.findAttribute("grid_column_span", attributes)

        let gridRowSpanN = 1
        if (gridRowSpan != null) {
            gridRowSpanN = Number(gridRowSpan.value)
        }

        let gridColumnSpanN = 1
        if (gridColumnSpan != null) {
            gridColumnSpanN = Number(gridColumnSpan.value)
        }

        if (gridRowStart != null) {
            let gridRowStartN = Number(gridRowStart.value) + 1

            html.style.gridRow = String(gridRowStartN) + "/" + "span " + String(gridRowSpanN)
        }
        
        if (gridColumnStart != null) {
            let gridColumnStartN = Number(gridColumnStart.value) + 1

            html.style.gridColumn = String(gridColumnStartN) + "/" + "span " + String(gridColumnSpanN)
        }
    }

    static setHover(html: HTMLElement, attributes:AttributeDto[]) {

        let onHover = AttributeHelperService.findGetAttributeValue("on_hover", attributes,"false")
        let onHoverBackgroundColor = AttributeHelperService.findGetAttributeValue("on_hover_background_color", attributes,"white")
        let onHoverForegroundColor = AttributeHelperService.findGetAttributeValue("on_hover_foreground_color", attributes,"black")
        let onHoverBorderColor = AttributeHelperService.findGetAttributeValue("on_hover_border_color", attributes,"white")
        let backgroundColor = AttributeHelperService.findGetAttributeValue("background_color", attributes,"white")
        let foregroundColor = AttributeHelperService.findGetAttributeValue("foreground_color", attributes,"black")
        let borderWidth = Number(AttributeHelperService.findGetAttributeValue("border_width", attributes, "0"))
        let borderColor = AttributeHelperService.findGetAttributeValue("border_color",attributes, "black")
        let borderStyle = "solid"

        if (onHover == "true") {
            html.onmouseenter = (event) => {
                html.style.backgroundColor = onHoverBackgroundColor
                html.style.color = onHoverForegroundColor

                AttributeHelperService.setBorder(html, borderWidth, onHoverBorderColor, borderStyle)
            }
            html.onmouseleave = (event) => {
                html.style.backgroundColor = backgroundColor
                html.style.color = foregroundColor

                AttributeHelperService.setBorder(html, borderWidth, borderColor, borderStyle)
            }

        }

    }

    static textAttributes(html: HTMLElement, attributes : AttributeDto[]) {
        let color = "black"
        let index = attributes.findIndex(item => item.key == "foreground_color")
        if (index >= 0) {
            color = String(attributes[index].value)
        }       
        html.style.color = color 

        let fontSize = String(12) + "px"
        index = attributes.findIndex(item => item.key == "font_size")
        if (index >= 0) {
            fontSize = String(attributes[index].value)
        }       
        html.style.fontSize = fontSize

    }

    static setAttributesDirectly(html: HTMLElement, attributes: AttributeDto[]) {
        attributes.forEach((attr : AttributeDto) => {
            (<any>html.style)[attr.key] = attr.value
        })
    }

    static findAttribute(key:string, attributes: AttributeDto[]) : AttributeDto | null {
      let value = null
      let index = attributes.findIndex(attr => attr.key == key)
      if (index >= 0) {
        value = attributes[index]
      }
      return value
    }

    static findGetAttributeValue(key: string, attributes: AttributeDto[], defaultValue: string) {
      let value = defaultValue
      let index = attributes.findIndex(attr => attr.key == key)
      if (index >= 0) {
        value = attributes[index].value
      }
      return value
    }

    static setAbsoulteRelativePositions(parentChildLayout:string, html:HTMLElement, child:ElementDto) {

        let posX = Number(AttributeHelperService.findGetAttributeValue("pos_x", child.attributes, "-1"))
        let posY = Number(AttributeHelperService.findGetAttributeValue("pos_y", child.attributes, "-1"))

        if (posX >= 0 && parentChildLayout == "absstatic") {
        html.style.left = String(posX) + "px"
        }
        if (posX >= 0 && parentChildLayout == "relstatic") {
        html.style.left = String(posX) + "%"
        }
        if (posY >= 0 && parentChildLayout == "absstatic") {
        html.style.top = String(posY) + "px"
        }
        if (posY >= 0 && parentChildLayout == "relstatic") {
        html.style.top = String(posY) + "%"
        }
        if (posY >= 0 || posX >= 0) {
        html.style.position = "absolute"
        }

        let gridRowStart = AttributeHelperService.findAttribute("grid_row", child.attributes)
        let gridColumnStart = AttributeHelperService.findAttribute("grid_column", child.attributes)

        if (gridRowStart == null && parentChildLayout == "grid") {
            html.style.gridRow = "1"
        }
        if (gridColumnStart == null && parentChildLayout == "grid") {
            html.style.gridColumn = "1"
        }

        let childLayout = AttributeHelperService.findAttribute("child_layout", child.attributes)
    }

    static setChildLayout(html:HTMLElement, attributes: AttributeDto[]) {
        let attribute = AttributeHelperService.findAttribute("child_layout", attributes)

        if (attribute != null) {
            let value = attribute?.value

            if (value == "grid") {
                html.style.display = "grid"
            } else if (value == "flex") {
                html.style.display = "flex"

                let flex_direction = AttributeHelperService.findAttribute("flex_direction", attributes)
                if (flex_direction != null) {
                    html.style.flexDirection = flex_direction.value
                } else {
                    html.style.flexDirection = "column"
                }
            } else if (value == "absstatic") {
                html.style.position = "absolute"
            } else if (value == "relstatic") {
                html.style.position = "absolute"
            }
        } else {
            html.style.display = "flex"
            html.style.flexDirection = "column"
        }
    }

}

