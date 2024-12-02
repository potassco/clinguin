import { Attribute, Injectable } from '@angular/core';
import { AttributeDto, ElementDto } from './types/json-response.dto';

@Injectable({
    providedIn: 'root'
})
export class AttributeHelperService {

    constructor() { }

    attrBackgroundColor(html: HTMLElement, attribute: AttributeDto) {
        let value = attribute.value

        html.style.backgroundColor = value
    }

    attrHeight(html: HTMLElement, attribute: AttributeDto) {
        let value = attribute.value + "px"
        html.style.height = value
    }

    attrWidth(html: HTMLElement, attribute: AttributeDto) {
        let value = attribute.value + "px"
        html.style.width = value
    }

    setDrag(html: HTMLElement, attributes: AttributeDto[]) {

        let draggable = this.findGetAttributeValue("draggable", attributes, "false")
        let draggable_bool = false
        if (draggable == "true") {
            draggable_bool = true
            html.style.cursor = "grab"
        }
        html.draggable = draggable_bool
        html.addEventListener("dragstart", (event) => {
            console.log("dragstart");
            if (event.dataTransfer) {
                event.dataTransfer.setData('dragged-id', html.id);
                // event.dataTransfer.setData('draggable', '');
            }
            html.style.opacity = "0.5";
            // document.documentElement.style.cursor = "grabbing";
            // store a ref. on the dragged elem
            // if (event.dataTransfer != null) {
            //     event.dataTransfer.effectAllowed = "copyMove";
            // }

        });
        html.addEventListener("dragend", (event) => {
            console.log("dragend");
            html.style.opacity = "1";
            // document.documentElement.style.cursor = "default";
        });
        html.addEventListener("dragover", (event) => {
            console.log("dragover");
            // if (event.dataTransfer != null) {
            //     console.log("not null");
            //     event.dataTransfer.dropEffect = "copy";
            // }
            // document.documentElement.style.cursor = "grab";

            // prevent default to allow drop
            event.preventDefault();
            // if (event.dataTransfer != null) {
            //     event.dataTransfer.effectAllowed = "copy";
            // }
        });
        html.addEventListener("leave", (event) => {
            console.log("leave");
            // html.style.opacity = "1";
            document.documentElement.style.cursor = "grab";

            // prevent default to allow drop
            event.preventDefault();
            // if (event.dataTransfer != null) {
            //     event.dataTransfer.effectAllowed = "copy";
            // }
        });
    }

    setBorderHelper(html: HTMLElement, attributes: AttributeDto[]) {

        let borderWidth = Number(this.findGetAttributeValue("border_width", attributes, "0"))
        let borderColor = this.findGetAttributeValue("border_color", attributes, "black")
        let borderStyle = "solid"

        this.setBorder(html, borderWidth, borderColor, borderStyle)
    }

    setBorder(html: HTMLElement, borderWidth: number, borderColor: string, borderStyle: string) {
        if (borderWidth > 0) {
            html.style.border = String(borderWidth) + "px " + borderStyle + " " + borderColor
        }

    }

    addAttributes(html: HTMLElement, attributes: AttributeDto[]) {

        let attr_dict = [
            { key: "background_color", value: this.attrBackgroundColor },
            { key: "height", value: this.attrHeight },
            { key: "width", value: this.attrWidth },
        ]

        attributes.forEach(attribute => {
            let index = attr_dict.findIndex(item => item.key == attribute.key)
            if (index >= 0) {
                attr_dict[index].value(html, attribute)
            }
        })

        this.setHover(html, attributes)
    }

    addGeneralAttributes(html: HTMLElement, attributes: AttributeDto[]) {
        this.setGrid(html, attributes)
        this.setBorderHelper(html, attributes)
        this.setDrag(html, attributes)
    }

    setGrid(html: HTMLElement, attributes: AttributeDto[]) {

        let gridRowStart = this.findAttribute("grid_row", attributes)
        let gridRowSpan = this.findAttribute("grid_row_span", attributes)
        let gridColumnStart = this.findAttribute("grid_column", attributes)
        let gridColumnSpan = this.findAttribute("grid_column_span", attributes)

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

    setHover(html: HTMLElement, attributes: AttributeDto[]) {

        let onHover = this.findGetAttributeValue("on_hover", attributes, "false")
        let onHoverBackgroundColor = this.findGetAttributeValue("on_hover_background_color", attributes, "white")
        let onHoverForegroundColor = this.findGetAttributeValue("on_hover_foreground_color", attributes, "black")
        let onHoverBorderColor = this.findGetAttributeValue("on_hover_border_color", attributes, "white")
        let backgroundColor = this.findGetAttributeValue("background_color", attributes, "white")
        let foregroundColor = this.findGetAttributeValue("foreground_color", attributes, "black")
        let borderWidth = Number(this.findGetAttributeValue("border_width", attributes, "0"))
        let borderColor = this.findGetAttributeValue("border_color", attributes, "black")
        let borderStyle = "solid"

        if (onHover == "true") {
            html.onmouseenter = (event) => {
                html.style.backgroundColor = onHoverBackgroundColor
                html.style.color = onHoverForegroundColor

                this.setBorder(html, borderWidth, onHoverBorderColor, borderStyle)
            }
            html.onmouseleave = (event) => {
                html.style.backgroundColor = backgroundColor
                html.style.color = foregroundColor

                this.setBorder(html, borderWidth, borderColor, borderStyle)
            }

        }

    }

    textAttributes(html: HTMLElement, attributes: AttributeDto[]) {
        // NOw IS SUPPOSED TO BE SET WITH THE CLASSES



        // let color = "black"
        // let index = attributes.findIndex(item => item.key == "foreground_color")
        // if (index >= 0) {
        //     color = String(attributes[index].value)
        // }
        // html.style.color = color

        // let fontSize = String(12) + "px"
        // let index = attributes.findIndex(item => item.key == "font_size")
        // if (index >= 0) {
        //     fontSize = String(attributes[index].value)
        // }
        // html.style.fontSize = fontSize

    }

    addClasses(html: Element, attributes: AttributeDto[], base_classes: string[], default_classes: string[], attrName: string = 'class') {

        base_classes.forEach(function (c) {
            if (html.classList.contains(c)) {
                html.classList.remove(c)
            }
            html.classList.add(c)
        })
        let added = false
        attributes.forEach(function (item) {
            if (item.key == attrName) {
                added = true
                let c = String(item.value)
                html.classList.add(c)
            }
        })

        if (!added) {
            default_classes.forEach(function (c) {
                html.classList.add(c)
            })
        }


    }

    setAttributesDirectly(html: HTMLElement, attributes: AttributeDto[]) {
        attributes.forEach((attr: AttributeDto) => {
            (<any>html.style)[attr.key] = attr.value
        })
    }

    findAttribute(key: string, attributes: AttributeDto[]): AttributeDto | null {
        let value = null
        let index = attributes.findIndex(attr => attr.key == key)
        if (index >= 0) {
            value = attributes[index]
        }
        return value
    }

    findGetAttributeValue(key: string, attributes: AttributeDto[], defaultValue: string) {
        let value = defaultValue
        let index = attributes.findIndex(attr => attr.key == key)
        if (index >= 0) {
            value = attributes[index].value
        }
        return value
    }

    setAbsoulteRelativePositions(parentChildLayout: string, html: HTMLElement, child: ElementDto) {

        let posX = Number(this.findGetAttributeValue("pos_x", child.attributes, "-1"))
        let posY = Number(this.findGetAttributeValue("pos_y", child.attributes, "-1"))

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
        if ((posY >= 0 || posX >= 0) && (parentChildLayout == "absstatic" || parentChildLayout == "relstatic")) {
            html.style.position = "absolute"
        }

        let gridRowStart = this.findAttribute("grid_row", child.attributes)
        let gridColumnStart = this.findAttribute("grid_column", child.attributes)

        if (gridRowStart == null && parentChildLayout == "grid") {
            html.style.gridRow = "1"
        }
        if (gridColumnStart == null && parentChildLayout == "grid") {
            html.style.gridColumn = "1"
        }

    }

    setChildLayout(html: HTMLElement, attributes: AttributeDto[]) {
        let attribute = this.findAttribute("child_layout", attributes)
        let flex_direction = this.findAttribute("flex_direction", attributes)

        if (attribute != null) {
            let value = attribute?.value

            if (value == "grid") {
                html.style.display = "grid"
            } else if (value == "flex") {
                html.style.display = "flex"

                if (flex_direction != null) {
                    html.style.flexDirection = flex_direction.value
                } else {
                    html.style.flexDirection = "column"
                }
            } else if (value == "absstatic") {
                html.style.position = "relative"
                html.style.display = "flex"
            } else if (value == "relstatic") {
                html.style.position = "relative"
                html.style.display = "flex"
            }
        } else {
            html.style.display = "flex"
            if (flex_direction != null) {
                html.style.flexDirection = flex_direction.value

            } else {
                html.style.flexDirection = "column"
            }
        }
    }

    setVisibility(html: HTMLElement, attributes: AttributeDto[]) {
        let visibilityAttribute = this.findAttribute("visibility", attributes)
        if (visibilityAttribute != null) {
            if (visibilityAttribute.value == "hidden" || visibilityAttribute.value == "collapse") {
                html.style.visibility = "collapse"
            } else if (visibilityAttribute.value == "shown" || visibilityAttribute.value == "visible") {
                html.style.visibility = "visible"
            }
        }
    }

}

