import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs/internal/Observable';
import { throwError } from 'rxjs/internal/observable/throwError';
import { ElementDto } from './types/json-response.dto';
import { ConfigService } from './config.service';
import { ContextItem } from './context.service';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(
    private http: HttpClient, private configService: ConfigService) {
      this.backend_URI = configService.serverUrl + ":" + configService.serverPort
     }

    private backend_URI = "http://localhost:8000"

    get(): Observable<ElementDto>{
      console.log(this.backend_URI)
      const response = this.http.get<ElementDto>(this.backend_URI,)
      
      .pipe(
        catchError((error:HttpErrorResponse,caught) => {
          // Handle the error here (e.g., log it or throw a custom error)
          console.error('Error occurred during the HTTP request:', error);
          return throwError(() => new Error(error.error)); 
        })
      );
      return response; 
    }

    post(policy: string, context: ContextItem[]): Observable<ElementDto>{
      const request = this.http.post<ElementDto>(this.backend_URI + "/backend", { function: policy, context: context })
      return request
    }
}
