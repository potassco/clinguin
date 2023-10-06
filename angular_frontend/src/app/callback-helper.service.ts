import { Injectable } from '@angular/core';
import { AttributeDto, WhenDto, ElementDto } from './types/json-response.dto';
import { DrawFrontendService } from './draw-frontend.service';
import { LocatorService } from './locator.service';
import { ContextService } from './context.service';
import { ElementLookupDto, ElementLookupService } from './element-lookup.service';
import { ChildBearerService } from './child-bearer.service';
import { ContextMenuService } from './context-menu.service';
import { hide } from '@popperjs/core';
import { isEmpty, throwError } from 'rxjs';


function aspArgumentSplitter(aspArguments: string) : string[] {

  let returnStrings : string[] = []
  let curString : string = ""

  let bracketLevel = 0

  for (let index = 0; index < aspArguments.length; index++) {
    let curChar = aspArguments.charAt(index)

    if (curChar == "(") {
      bracketLevel += 1
      curString += curChar
    } else if (curChar == ")") {
      bracketLevel -= 1
      curString += curChar

      if (bracketLevel < 0) {
        console.log("ERROR - BRACKE LEVEL LOWER THAN 0")
        break
      }
    } else if (curChar == "," && bracketLevel == 0) {
      returnStrings.push(curString)
      curString = ""
    } else {
      curString += curChar
    }
  }

  returnStrings.push(curString)

  return returnStrings
}

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

function handleRightClick(html: HTMLElement, when:WhenDto, event: Event) {
  event.preventDefault()
  event.stopPropagation()

  if (hideAllContextMenus() == true) {
    return
  }

  let contextMenuService = LocatorService.injector.get(ContextMenuService)

  let result = contextMenuService.retrieveContextValue(when.policy)

  if (result != null) {
    if ("pageX" in event && "pageY" in event && typeof event.pageX == "number" && typeof event.pageY == "number") {

      let contextMenu = document.getElementById(when.policy)

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
 

function handleUpdate(when:WhenDto, event: Event) {
  let elementLookupService = LocatorService.injector.get(ElementLookupService)

  let policy = when.policy

  policy = policy.substring(1)
  policy = policy.slice(0,-1)

  let splits = aspArgumentSplitter(policy)

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
    console.log("COULD NOT FIND ELEMENT FOR when:" + id + "::" + key + "::" + value)
  }


}

function replaceContext(policy_string:string, optional:boolean){
  let contextService = LocatorService.injector.get(ContextService)
  let regex = /_context_value\(([^)]*)\)/
  if (optional){
    regex = /_context_value_optional\(([^)]*)\)/
  }

  let match = regex.exec(policy_string)
  while(match != null) {
    let match_group = match[1]

    let new_value = contextService.retrieveContextValue(match_group)
    if (new_value.length == 0 && !optional){
      throw new Error("Missing required value for " + match_group);      
    }
    function isNumber(s:string) {
      return /^[0-9]*$/.test(s);
    }

    if (!isNumber(new_value) && new_value.length>0) {
      if ( new_value[0] === new_value[0].toUpperCase()){
        new_value = '"'+new_value+'"'
      }
    } 
    policy_string = policy_string.replace(regex, new_value)
    
    match = regex.exec(policy_string)
  }
  return policy_string
}
function handleCallback(when:WhenDto, event: Event) {
  let frontendService = LocatorService.injector.get(DrawFrontendService)

  let policy_string = when.policy

  policy_string = replaceContext(policy_string, true)
  policy_string = replaceContext(policy_string, false)

  when.policy = policy_string

  frontendService.policyPost(when)
}

function handleContext(when:WhenDto, event: Event | null) {
  let contextService = LocatorService.injector.get(ContextService)
  let policy = when.policy

  if (policy[0]=='('){
    policy = policy.substring(1)
    policy = policy.slice(0,-1)

    let splits = aspArgumentSplitter(policy)
    if (splits.length >= 2) {
      if (splits.length > 2) {
        console.log("ATTENTION, CONTEXT LENGTH GREATER THAN 2 FOR")
        console.log(when)
      }
      let key = splits[0]
      let value = splits[1]

      if (event!=null){

        let regex = /_value/g
        let eventTarget : EventTarget | null = event.target
    
        if (eventTarget != null && "value" in eventTarget) {
          let match = value.match(regex)
    
          if (match != null && typeof eventTarget.value === "string") {
            if (eventTarget.value == "") {
              console.log("EVENT TARGET IS EMPTY")
              // DO NOTHING IF EMPTY!
              return
            }
            value = value.replace("_value", eventTarget.value)
          }
        }
      }

      for (let index = 2; index < splits.length; index++) {
          value = value + "," + splits[index]
      }
      contextService.addContext(key, value)
      return
    }
  } 

  let message = "The value of context event should be a tuple of size 2, but got " +when.policy 
  console.error(message)
  let frontendService = LocatorService.injector.get(DrawFrontendService)
  frontendService.postMessage(message,"warning")
}

@Injectable({
  providedIn: 'root'
})
export class CallBackHelperService {

  constructor(private frontendService: DrawFrontendService) {
    document.onclick = defaultClickContextHandler; 
    document.oncontextmenu = defaultClickContextHandler; 
   }

    findCallback(action: string, callbacks: WhenDto[]): WhenDto | null {
      let value = null
      let index = callbacks.findIndex(callback => callback.actionType == action)
      if (index >= 0) {
        value = callbacks[index]
      }
      return value
    }
 
    setCallbacks(html: HTMLElement, dos:WhenDto[]) {
      this.handleEvent(html, dos, "click", "click")
      this.handleEvent(html, dos, "input", "input")
      this.handleEvent(html, dos, "right_click", "contextmenu")
      this.handleEvent(html, dos, "load", "load")
    }

    handleEvent(html: HTMLElement, dos:WhenDto[], supportedAttributeName:string = "", htmlEventName:string = "") {
      
      let allEvents:WhenDto[] = []
      dos.forEach((when:WhenDto) => {
        if (when.actionType == supportedAttributeName) {
          allEvents.push(when)
        }
      })
      
      if (allEvents.length > 0 && htmlEventName != "") {
        if(supportedAttributeName=="load"){
          console.warn("In load")
          allEvents.forEach((when:WhenDto) => {
            if (when.interactionType == "context") {
              handleContext(when, null)
            }
          })
          return
        }
        if (supportedAttributeName == "click") {
          html.style.cursor = "pointer"
        }
        html.addEventListener(htmlEventName,function(event: Event){
          allEvents.sort( function (a, b) {
            if (a.interactionType < b.interactionType) {
              return 1;
            }
            if (a.interactionType > b.interactionType) {
              return -1;
            }
            return 0;
          });

          const updates = allEvents.filter((w) => w.interactionType == "update"|| w.interactionType == "context")
          const context = allEvents.filter((w) => w.interactionType == "context")
          const call = allEvents.filter((w) => w.interactionType == "call" || w.interactionType == "callback")
          const context_menu = allEvents.filter((w) => w.interactionType == "show_context_menu" )
          
          context_menu.forEach((when:WhenDto) => {
            try{
                handleRightClick(html,when, event)
            }catch(error:any){
              let frontendService = LocatorService.injector.get(DrawFrontendService)
              frontendService.postMessage(error.message,"warning")
            }
          })

          updates.forEach((when:WhenDto) => {
            try{
                handleUpdate(when, event)
            }catch(error:any){
              let frontendService = LocatorService.injector.get(DrawFrontendService)
              frontendService.postMessage(error.message,"warning")
            }
          })

          context.forEach((when:WhenDto) => {
            try{
                handleContext(when, event)
            }catch(error:any){
              let frontendService = LocatorService.injector.get(DrawFrontendService)
              frontendService.postMessage(error.message,"warning")
            }
          })

          if (call.length>1) {
            call[0].policy = "(" + call.map(x=>{return x.policy}).join(',') + ")"
          }
          call.forEach((when:WhenDto) => {
            try{
                handleCallback(call[0],event)
            }catch(error:any){
              let frontendService = LocatorService.injector.get(DrawFrontendService)
              frontendService.postMessage(error.message,"warning")
            }
          })
        })

      }
    }
    
}



