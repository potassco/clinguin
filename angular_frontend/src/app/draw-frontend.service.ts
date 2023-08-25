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

    constructor(private httpService: HttpService) {
    }

    initialGet() : void {
        this.httpService.get().subscribe(
        {next: (data:ElementDto) => {
            this.frontendJson.next(data)
        }})
    }

    policyPost(callback: CallbackDto) : void {
        this.httpService.post(callback.policy).subscribe(
        {next: (data:ElementDto) => {
            this.frontendJson.next(data)
        }})
    }




}