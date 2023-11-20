import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs/internal/Observable';
import { throwError } from 'rxjs/internal/observable/throwError';
import { ElementDto } from './types/json-response.dto';
import { ConfigService } from './config.service';
import { ContextItem, ContextService } from './context.service';
import { ModalRefService } from './modal-ref.service';
import { ElementLookupService } from './element-lookup.service';
import { ContextMenuService } from './context-menu.service';
import { DrawFrontendService } from './draw-frontend.service';
import { LocatorService } from './locator.service';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(
    private http: HttpClient, private configService: ConfigService, private modalRefService: ModalRefService, private elementLookupService: ElementLookupService, private contextService: ContextService, private contextMenuService: ContextMenuService) {
      this.backend_URI = configService.serverUrl + ":" + configService.serverPort
     }

    private backend_URI = "http://localhost:8000"

    get(): Observable<ElementDto>{
      this.modalRefService.closeRemoveAllModals()
      this.elementLookupService.clearElementLookupDict()
      this.contextService.clearContext()
      this.contextMenuService.removeAllContextMenus()
      let frontendService = LocatorService.injector.get(DrawFrontendService)


      const response = this.http.get<ElementDto>(this.backend_URI,)
      
      .pipe(
        catchError((error:HttpErrorResponse,caught) => {
          console.error('Error occurred during the HTTP request:', error);
          frontendService.postMessage("error connection")
          return throwError(() => new Error(error.error)); 
        })
      );
      
      frontendService.lastData
      return response; 
    }

    post(policy: string, context: ContextItem[]): Observable<ElementDto>{
      let clonedContext : ContextItem[] = []
      context.forEach(val => clonedContext.push(Object.assign({}, val)));

      this.modalRefService.closeRemoveAllModals()
      this.elementLookupService.clearElementLookupDict()
      this.contextService.clearContext()
      this.contextMenuService.removeAllContextMenus()


      let request = null
      if (clonedContext.length > 0) {
        request = this.http.post<ElementDto>(this.backend_URI + "/backend", { function: policy, context: clonedContext })
      } else {
        request = this.http.post<ElementDto>(this.backend_URI + "/backend", { function: policy})
      }
      return request
    }
}
