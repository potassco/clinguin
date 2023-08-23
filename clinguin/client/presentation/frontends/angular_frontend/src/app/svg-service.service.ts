import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { GraphRequest, GraphResponse } from './types/messageTypes';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs/internal/Observable';
import { of } from 'rxjs/internal/observable/of';
import { throwError } from 'rxjs/internal/observable/throwError';

@Injectable({
  providedIn: 'root'
})
export class SvgServiceService {

  constructor(
    private http: HttpClient) { }

    private backend_URI = "http://localhost:8000"

    get(): Observable<GraphResponse>{
      const resp = this.http.get<GraphResponse>(this.backend_URI,)
      
      .pipe(
        catchError((error:HttpErrorResponse,caught) => {
          // Handle the error here (e.g., log it or throw a custom error)
          console.error('Error occurred during the HTTP request:', error);
          return throwError(() => new Error(error.error)); 
        })
      );
      return resp; 
    }

    post(graphRequest:GraphRequest): Observable<GraphResponse>{
      const resp = this.http.post<GraphResponse>(this.backend_URI+"/backend",graphRequest)
      .pipe(
        catchError((error:HttpErrorResponse,caught) => {
          // Handle the error here (e.g., log it or throw a custom error)
          console.error('Error occurred during the HTTP request:', error);
          return throwError(() => new Error(error.error)); 
        })
      );
      return resp; 
    }
    
    mock(graphRequest:GraphRequest): Observable<GraphResponse> {
      const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
      const options = { headers }
      const resp = this.http.post<GraphRequest>(this.backend_URI+"/mock/",graphRequest,{...headers})
      
      .pipe(
        catchError((error,caught) => {
          // Handle the error here (e.g., log it or throw a custom error)
          console.error('Error occurred during the HTTP request:', error);
          return of(error)
        })
      );
      return resp;
    }
}
