import { ComponentRef, Injectable, ViewContainerRef } from "@angular/core";
import { ComponentCreationService } from "./component-creation.service";
import { ElementDto } from "./types/json-response.dto";
import { ElementLookupService } from "./element-lookup.service";
import { AttributeHelperService } from "./attribute-helper.service";

@Injectable({
  providedIn: 'root'
})
export class ChildBearerService {

    constructor(private componentService: ComponentCreationService, private elementLookupService: ElementLookupService, private attributeService: AttributeHelperService) {}

    bearChild(child : ViewContainerRef, item: ElementDto, childLayout : string): ComponentRef<any> | null {
        let my_comp = this.componentService.componentCreation(child, item.type)
        
        if (my_comp != null) {
          my_comp.setInput("element",item)
          my_comp.setInput("parentLayout", childLayout)
          let html: HTMLElement = <HTMLElement>my_comp.location.nativeElement
          html.id = item.id

          this.elementLookupService.addElementTagHTML(item.id, html, item)

          this.setAllTagAttributes(html, item, childLayout)
        }

        return my_comp
    }

    setAllTagAttributes(html:HTMLElement, item:ElementDto, childLayout:string) { 
        if (item.type != "button") {
            this.attributeService.setAbsoulteRelativePositions(childLayout, html, item)
        }
        this.setChildTagAttributes(html, item)
    }

    setChildTagAttributes(html:HTMLElement, item:ElementDto) {
      //if (item.type != "button") {
        this.attributeService.setAttributesDirectly(html, item.attributes)
        this.attributeService.addGeneralAttributes(html, item.attributes)

        this.attributeService.addAttributes(html, item.attributes)
        if (item.type == "container") {
          this.attributeService.setChildLayout(html, item.attributes)
          this.attributeService.setVisibility(html, item.attributes)
          this.attributeService.addClasses(html, item.attributes, [], ["p-2"])
        }
        

      //}

    }

}
