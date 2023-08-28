import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs/internal/Observable';
import { throwError } from 'rxjs/internal/observable/throwError';
import { CallbackDto, ElementDto } from './types/json-response.dto';
import { Subject } from 'rxjs';
import { HttpService } from './http.service';

@Injectable({
  providedIn: 'root'
})
export class DrawFrontendService {

    frontendJson : Subject<ElementDto> = new Subject()
    menuBar: Subject<ElementDto> = new Subject()
    messageLists: Subject<ElementDto[]> = new Subject()

    constructor(private httpService: HttpService) {
    }

    initialGet() : void {
        this.httpService.get().subscribe(
        {next: (data:ElementDto) => {
            this.detectCreateMenuBar(data)

            let messageList : ElementDto[] = []
            this.getAllMessages(data, messageList)
            this.messageLists.next(messageList)

            this.frontendJson.next(data)
        }})
    }

    policyPost(callback: CallbackDto) : void {
        this.httpService.post(callback.policy).subscribe(
        {next: (data:ElementDto) => {
            this.detectCreateMenuBar(data)

            let messageList : ElementDto[] = []
            this.getAllMessages(data, messageList)
            this.messageLists.next(messageList)

            this.frontendJson.next(data)
        }})
    }


    detectCreateMenuBar(element:ElementDto) {
        if (element.type == "menu_bar") {
            this.menuBar.next(element)
        } else {
            element.children.forEach(child => {
                this.detectCreateMenuBar(child)
            })
        }
    }

    getAllMessages(element:ElementDto, messageList:ElementDto[]) {

        if (element.type == "message") {
            messageList.push(element)
        } else {
            element.children.forEach(child => {
                this.getAllMessages(child, messageList)
            })
        }

    }




}