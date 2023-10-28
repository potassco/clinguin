import { Injectable } from "@angular/core";
import { ElementDto } from "./types/json-response.dto";

@Injectable({
  providedIn: 'root'
})
export class ElementLookupService {

    elementLookup : ElementLookupDto[] = []

    private findElementIndex(key:string) : number {
        let foundIndex : number = -1
        for (let index = 0; index < this.elementLookup.length; index++) {
            let item = this.elementLookup[index]

            if (item.id == key) {
                foundIndex = index
            }

        }       

        return foundIndex
    }

    addElementObject(key: string, val: Object, element: ElementDto) {

        let foundIndex = this.findElementIndex(key)

        if (foundIndex < 0) {
            let newElemement = this.initializeElementLookupDtoNullTagHTML(key, element, val)
            this.elementLookup.push(newElemement)
        } else { // result != undefined
            this.elementLookup[foundIndex].object = val
        }
    }
    
    addElementTagHTML(key: string, htmlTag: HTMLElement|null, element: ElementDto) {
        
        let foundIndex = this.findElementIndex(key)
        
        if (foundIndex < 0) {
            let newElemement = this.initializeElementLookupDtoNullObject(key, element, htmlTag)
            this.elementLookup.push(newElemement)
        } else { // result != undefined
            this.elementLookup[foundIndex].tagHtml = htmlTag
        }
    }

    addElementAll(key:string, object: Object, htmlTag: HTMLElement, element: ElementDto) {
        let result = this.elementLookup.find((item: ElementLookupDto) => {key == item.id})
        if (result == undefined) {
            let newElemement = this.initializeElementLookupDtoAll(key, object, element, htmlTag)
            this.elementLookup.push(newElemement)
        } else { // result != undefined
            if (result.tagHtml == null) {
                result.tagHtml = htmlTag
            }
            if (result.object == null) {
                result.object = null
            }
        }
    }

    getElement(key:string) : ElementLookupDto | null {
        let result =  this.elementLookup.find((item: ElementLookupDto) => item.id == key)

        if (result != undefined) {
            return result
        } else {
            return null
        }
    }


    private initializeElementLookupDtoAll(id:string, object:Object, element:ElementDto, tagHTML:HTMLElement) {
        return new ElementLookupDto(id, object, element, tagHTML)
    }

    private initializeElementLookupDtoNullObject(id:string, element:ElementDto, tagHTML:HTMLElement|null) {
        return new ElementLookupDto(id, null, element, tagHTML)
    }
        
    private initializeElementLookupDtoNullTagHTML(id:string,  element:ElementDto, object: Object) {
        return new ElementLookupDto(id, object, element, null)
    }

    clearElementLookupDict() : void {
        this.elementLookup.length = 0
    }
}

export class ElementLookupDto {
    id! : string
    object! : Object | null
    element! : ElementDto
    tagHtml! : HTMLElement | null

    constructor(id : string, object : Object | null, element: ElementDto, tagHtml : HTMLElement | null) {
        this.id = id
        this.object = object
        this.element = element
        this.tagHtml = tagHtml
    }

}

