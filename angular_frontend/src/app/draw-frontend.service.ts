import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs/internal/Observable';
import { throwError } from 'rxjs/internal/observable/throwError';
import { WhenDto, ElementDto, JsonResponse } from './types/json-response.dto';
import { Subject } from 'rxjs';
import { HttpService } from './http.service';
import { ServerRequest } from './types/server-request';
import { ContextService } from './context.service';
import { LocatorService } from './locator.service';
import { ElementLookupDto, ElementLookupService } from './element-lookup.service';

@Injectable({
    providedIn: 'root'
})
export class DrawFrontendService {

    frontendJson: Subject<ElementDto> = new Subject()
    menuBar: Subject<ElementDto> = new Subject()
    messageLists: Subject<ElementDto[]> = new Subject()
    contextMenus: Subject<ElementDto[]> = new Subject()

    lastData: ElementDto | null = null

    private backend_URI = "http://localhost:8000"

    constructor(private httpService: HttpService, private httpClient: HttpClient, private contextService: ContextService) {
    }

    initialGet(): void {
        let loader = document.getElementById("loader")

        loader?.removeAttribute("hidden")

        let errorIcon = document.getElementById("error")

        errorIcon?.setAttribute("hidden", "true");

        this.httpService.get().pipe(
            catchError((error: HttpErrorResponse) => {
                this.postMessage(`Connection Error`);
                loader?.setAttribute("hidden", "true");
                errorIcon?.removeAttribute("hidden");
                return throwError(() => new Error(error.error));

            })
        ).subscribe(
            {
                next: (data: JsonResponse) => {
                    this.lastData = data.ui
                    this.frontendJson.next(data.ui)
                    loader?.setAttribute("hidden", "true")
                }
            })

    }

    operationPost(callback: WhenDto): void {

        let context = this.contextService.getContext()
        let loader = document.getElementById("loader")
        loader?.removeAttribute("hidden")

        let errorIcon = document.getElementById("error")

        errorIcon?.setAttribute("hidden", "true");

        this.httpService.post(callback.operation, context).pipe(
            catchError((error: HttpErrorResponse) => {
                this.postMessage(`Connection Error`);
                loader?.setAttribute("hidden", "true");
                errorIcon?.removeAttribute("hidden");
                return throwError(() => new Error(error.error));

            })
        ).subscribe(
            {
                next: (data: JsonResponse) => {
                    this.lastData = data.ui
                    this.frontendJson.next(data.ui)
                    loader?.setAttribute("hidden", "true")
                }
            })

    }

    detectCreateMenuBar(element: ElementDto) {
        if (element.type == "menu_bar") {
            this.menuBar.next(element)
        } else {
            element.children.forEach(child => {
                this.detectCreateMenuBar(child)
            })
        }
    }

    getAllMessagesContextMenus(element: ElementDto, messageList: ElementDto[], contextMenuList: ElementDto[]) {

        if (element.type == "message") {
            messageList.push(element)
        } else if (element.type == "context_menu") {
            contextMenuList.push(element)
        } else {
            element.children.forEach(child => {
                this.getAllMessagesContextMenus(child, messageList, contextMenuList)
            })
        }
    }

    postMessage(message: string, type: string = "danger") {
        let messageList: ElementDto[] = [this.getErrorMessage(message)]
        this.messageLists.next(messageList)
    }

    getErrorMessage(message: string, type: string = "danger") {
        let messageElement: ElementDto = {
            "id": "client_error",
            "type": "message",
            "parent": "window",
            "attributes": [
                {
                    "id": "client_error",
                    "key": "message",
                    "value": message
                },
                {
                    "id": "client_error",
                    "key": "title",
                    "value": "Error"
                },
                {
                    "id": "client_error",
                    "key": "type",
                    "value": type
                }
            ],
            "when": [],
            "children": []
        }
        return messageElement
    }
}
