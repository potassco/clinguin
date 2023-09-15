import { Injectable } from '@angular/core';
import { AttributeDto, DoDto, ElementDto } from './types/json-response.dto';
import { DrawFrontendService } from './draw-frontend.service';
import { LocatorService } from './locator.service';
import { ContextService } from './context.service';
import { ElementLookupDto, ElementLookupService } from './element-lookup.service';
import { ChildBearerService } from './child-bearer.service';
import { ContextMenuService } from './context-menu.service';
import { hide } from '@popperjs/core';

function defaultClickContextHandler(event: Event) {
  let contextMenuService = LocatorService.injector.get(ContextMenuService)

  if (contextMenuService.contextMenus.length > 0) {
    event.preventDefault()
    event.stopPropagation()

    if (hideAllContextMenus() == true) {
      return
    }   
  }
}

function hideAllContextMenus() : boolean { 
  let contextMenuService = LocatorService.injector.get(ContextMenuService)
  let anyWasOpen = false

  contextMenuService.contextMenus.forEach((item: {key:string, contextMenu:ElementDto}) => {
    let contextMenu = document.getElementById(item.key)

    if (contextMenu != null && contextMenu.style.display == "block") {
      contextMenu.style.display = "none"
      anyWasOpen = true
    }
  })

  return anyWasOpen
} 

function handleRightClick(html: HTMLElement, do_:DoDto, event: Event) {
  event.preventDefault()
  event.stopPropagation()

  if (hideAllContextMenus() == true) {
    return
  }

  let contextMenuService = LocatorService.injector.get(ContextMenuService)

  let result = contextMenuService.retrieveContextValue(do_.policy)

  if (result != null) {
    if ("pageX" in event && "pageY" in event && typeof event.pageX == "number" && typeof event.pageY == "number") {

      /*
      const x = event.offsetX;
      const y = event.offsetY - 15;
      let style_display = "block";
      let style_top = y + "px";
      let style_left = x + "px";
      */

      let contextMenu = document.getElementById(do_.policy)

      if (contextMenu != null) {
        if (contextMenu.style.display == "block"){ 
          contextMenu.style.display = "none"
        } else { 
          contextMenu.style.display = 'block'; 
          contextMenu.style.left = event.pageX + "px"; 
          contextMenu.style.top = event.pageY + "px"; 
      } 

      }

    }
  }
  

}
 

function handleUpdate(do_:DoDto, event: Event) {
  console.log(do_)
  let elementLookupService = LocatorService.injector.get(ElementLookupService)

  let policy = do_.policy

  policy = policy.substring(1)
  policy = policy.slice(0,-1)
  let splits = policy.split(",")

  let id = splits[0]
  let key = splits[1]
  let value = splits[2]

  let elementLookup : ElementLookupDto | null = elementLookupService.getElement(id)

  if (elementLookup != null) {
    let tmpAttributes = elementLookup.element.attributes
    let found = false

    for (let index in tmpAttributes) {
      let attribute : AttributeDto = tmpAttributes[index]

      if (attribute.key == key) {
        found = true
        tmpAttributes[index] = {"id":id, "key":key,"value":value}
      }
    }

    if (found == false) {
      tmpAttributes.push({"id":id, "key":key,"value":value})
    }

    elementLookup.element.attributes = tmpAttributes

    if (elementLookup.object != null) {
      if ("setAttributes" in elementLookup.object) {
        if (elementLookup.object.setAttributes != undefined && typeof elementLookup.object.setAttributes === 'function') {
          elementLookup.object.setAttributes(tmpAttributes)
        }
      }
    }
    if (elementLookup.tagHtml != null) {
      let childBearerService = LocatorService.injector.get(ChildBearerService)

      childBearerService.setChildTagAttributes(elementLookup.tagHtml, elementLookup.element)
    }

  } else {
    console.log("COULD NOT FIND ELEMENT FOR do_:" + id + "::" + key + "::" + value)
  }


}
  
function handleCallback(do_:DoDto, event: Event) {
  let frontendService = LocatorService.injector.get(DrawFrontendService)
  let contextService = LocatorService.injector.get(ContextService)

  let regex = /_value_context\(([^)]*)\)/
  let policy_string = do_.policy

  let match = regex.exec(policy_string)
  while(match != null) {
    let match_group = match[1]

    let new_value = contextService.retrieveContextValue(match_group)

    policy_string = policy_string.replace(regex, new_value)
    
    match = regex.exec(policy_string)
  }

  do_.policy = policy_string

  frontendService.policyPost(do_)
  }

function handleContext(do_:DoDto, event: Event) {
  let contextService = LocatorService.injector.get(ContextService)
   
  let policy = do_.policy

  policy = policy.substring(1)
  policy = policy.slice(0,-1)
  let splits = policy.split(",")

  let key = splits[0]

  let value = splits[1]

  if (value == "_value") {
    let eventTarget : EventTarget | null = event.target

    if (eventTarget != null && "value" in eventTarget) {
      if (typeof eventTarget.value === "string") {
        value = eventTarget.value
      }
    }
  }

  for (let index = 2; index < splits.length; index++) {
      value = value + "," + splits[index]
  }

  contextService.addContext(key, value)
}

@Injectable({
  providedIn: 'root'
})
export class CallBackHelperService {

  constructor(private frontendService: DrawFrontendService) {
    document.onclick = defaultClickContextHandler; 
    document.oncontextmenu = defaultClickContextHandler; 
   }

    findCallback(action: string, callbacks: DoDto[]): DoDto | null {
      let value = null
      let index = callbacks.findIndex(callback => callback.actionType == action)
      if (index >= 0) {
        value = callbacks[index]
      }
      return value
    }
 
    setCallbacks(html: HTMLElement, dos:DoDto[]) {
      this.handleEvent(html, dos, "click", "click")
      this.handleEvent(html, dos, "type", "input")
      this.handleEvent(html, dos, "right_click", "contextmenu")
    }

    handleEvent(html: HTMLElement, dos:DoDto[], supportedAttributeName:string = "", htmlEventName:string = "") {
      
      let allClicks:DoDto[] = []
      dos.forEach((do_:DoDto) => {
        if (do_.actionType == supportedAttributeName) {
          allClicks.push(do_)
        }
      })

      if (allClicks.length > 0 && htmlEventName != "") {

        html.addEventListener(htmlEventName,function(event: Event){

          allClicks.forEach((do_:DoDto) => {
            if (do_.interactionType == "update") {
              console.log("UPDATE")
              handleUpdate(do_, event)
            } else if (do_.interactionType == "context") {
              handleContext(do_, event)
            } else if (do_.interactionType == "call" || do_.interactionType == "callback") {
              handleCallback(do_, event)
            } else if (do_.interactionType == "show_context_menu") {
              handleRightClick(html, do_, event)
           }
          })
        })

      }
    }
    
}



