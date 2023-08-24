import { Injectable } from '@angular/core';
import { AttributeDto } from './types/json-response.dto';

@Injectable({
  providedIn: 'root'
})
export class AttributeHelperService {

  constructor() { }

    static attr_grid_row(html:HTMLElement, attribute: AttributeDto) {
        let value = String(Number(attribute.value) + 1)

        html.style.gridRowStart = value
        html.style.gridRowEnd = value
    }

    static attr_grid_column(html:HTMLElement, attribute: AttributeDto) {
        let value = String(Number(attribute.value) + 1)

        html.style.gridColumnStart = value
        html.style.gridColumnEnd = value
    }

    static attr_background_color(html:HTMLElement, attribute: AttributeDto) {
        let value = attribute.value

        html.style.backgroundColor = value
    }

    static attr_height(html:HTMLElement, attribute: AttributeDto) {
        let value = attribute.value + "px"
        html.style.height = value
    }

    static attr_width(html:HTMLElement, attribute: AttributeDto) {
        let value = attribute.value + "px"
        html.style.width = value
    }

    static attr_child_layout(html:HTMLElement, attribute: AttributeDto) {
        let value = attribute.value 

        if (value == "grid") {
            html.style.display = "grid"
        } else if (value == "flex") {
            html.style.display = "flex"
            html.style.flexDirection = "column"
        }
    }

    static add_attributes(html:HTMLElement, attributes : AttributeDto[]) {

        let attr_dict = [
            {key:"grid_row", value:AttributeHelperService.attr_grid_row},
            {key:"grid_column", value:AttributeHelperService.attr_grid_column},
            {key:"background_color",value:AttributeHelperService.attr_background_color},
            {key:"height", value:AttributeHelperService.attr_height},
            {key:"width", value:AttributeHelperService.attr_width},
            {key:"child_layout", value:AttributeHelperService.attr_child_layout}
        ]

        attributes.forEach(attribute => {
            let index = attr_dict.findIndex(item => item.key == attribute.key)
            if (index >= 0) {
                attr_dict[index].value(html,attribute)
            }
        })

    }
}

