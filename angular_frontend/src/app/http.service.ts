import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs/internal/Observable';
import { throwError } from 'rxjs/internal/observable/throwError';
import { ElementDto } from './types/json-response.dto';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(
    private http: HttpClient) { }

    private backend_URI = "http://localhost:8000"

    get(): Observable<ElementDto>{
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
}
