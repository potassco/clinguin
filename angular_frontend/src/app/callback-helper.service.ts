import { Injectable } from '@angular/core';
import { AttributeDto, DoDto, ElementDto } from './types/json-response.dto';
import { DrawFrontendService } from './draw-frontend.service';

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

        let onHoverCallback = this.findCallback("click", callbacks)
        if (onHoverCallback != null) {
            html.style.cursor = "pointer"

            html.onclick = (event) => {
                if (onHoverCallback != null) {
                    this.frontendService.policyPost(onHoverCallback)
                }
            }
        }
    } 
}



