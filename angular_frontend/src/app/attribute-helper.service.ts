import { Injectable } from '@angular/core';
import { AttributeDto } from './types/json-response.dto';

@Injectable({
  providedIn: 'root'
})
export class AttributeHelperService {

  constructor() { }

    static attrGridRow(html:HTMLElement, attribute: AttributeDto) {
        let value = String(Number(attribute.value) + 1)

        html.style.gridRowStart = value
        html.style.gridRowEnd = value
    }

    static attrGridColumn(html:HTMLElement, attribute: AttributeDto) {
        let value = String(Number(attribute.value) + 1)

        html.style.gridColumnStart = value
        html.style.gridColumnEnd = value
    }

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

    static attrChildLayout(html:HTMLElement, attribute: AttributeDto) {
        let value = attribute.value 

        if (value == "grid") {
            html.style.display = "grid"
        } else if (value == "flex") {
            html.style.display = "flex"
            html.style.flexDirection = "column"
        }
    }

    static set_border(html:HTMLElement, attributes: AttributeDto[]) {

        let border_width = 0
        let index = attributes.findIndex(item => item.key == "border_width")
        if (index >= 0) {
            border_width = Number(attributes[index].value)
        }       

        let border_color = "black"
        index = attributes.findIndex(item => item.key == "border_color")
        if (index >= 0) {
            border_color = attributes[index].value
        }       

        let border_style = "solid"

        if (border_width > 0) {
            html.style.border = String(border_width) + "px " + border_style + " " + border_color
        }
    }

    static addAttributes(html:HTMLElement, attributes : AttributeDto[]) {

        let attr_dict = [
            {key:"grid_row", value:AttributeHelperService.attrGridRow},
            {key:"grid_column", value:AttributeHelperService.attrGridColumn},
            {key:"background_color",value:AttributeHelperService.attrBackgroundColor},
            {key:"height", value:AttributeHelperService.attrHeight},
            {key:"width", value:AttributeHelperService.attrWidth},
            {key:"child_layout", value:AttributeHelperService.attrChildLayout}
        ]

        attributes.forEach(attribute => {
            let index = attr_dict.findIndex(item => item.key == attribute.key)
            if (index >= 0) {
                attr_dict[index].value(html,attribute)
            }
        })

        AttributeHelperService.set_border(html, attributes)
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
        console.log(attributes)
        attributes.forEach((attr : AttributeDto) => {
            (<any>html.style)[attr.key] = attr.value
        })
    }
}

