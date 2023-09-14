import { Injectable } from '@angular/core';
import { AttributeDto, DoDto, ElementDto } from './types/json-response.dto';
import { DrawFrontendService } from './draw-frontend.service';
import { LocatorService } from './locator.service';
import { ContextService } from './context.service';
import { ElementLookupDto, ElementLookupService } from './element-lookup.service';
import { ChildBearerService } from './child-bearer.service';

function handleUpdate(do_:DoDto) {
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
  
function handleCallback(do_:DoDto) {
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

function handleContext(do_:DoDto) {
  let contextService = LocatorService.injector.get(ContextService)
   
  let policy = do_.policy

  policy = policy.substring(1)
  policy = policy.slice(0,-1)
  let splits = policy.split(",")

  let key = splits[0]

  let value = splits[1]
  for (let index = 2; index < splits.length; index++) {
      value = value + "," + splits[index]
  }

  contextService.addContext(key, value)
}

@Injectable({
  providedIn: 'root'
})
export class CallBackHelperService {

  constructor(private frontendService: DrawFrontendService) { }

    findCallback(action: string, callbacks: DoDto[]): DoDto | null {
      let value = null
      let index = callbacks.findIndex(callback => callback.actionType == action)
      if (index >= 0) {
        value = callbacks[index]
      }
      return value
    }
 
    setCallbacks(html: HTMLElement, callbacks:DoDto[]) {

      let allClicks:DoDto[] = []
      callbacks.forEach((do_:DoDto) => {
        if (do_.actionType == "click") {
          allClicks.push(do_)
        }
      })

      if (allClicks.length > 0) {

        html.addEventListener("click",function(){
          allClicks.forEach((do_:DoDto) => {
            if (do_.interactionType == "update") {
              handleUpdate(do_)
            } else if (do_.interactionType == "context") {
              handleContext(do_)
            } else if (do_.interactionType == "call" || do_.interactionType == "callback") {
              handleCallback(do_)
            }
          })
        })

      }
    }
    
}



