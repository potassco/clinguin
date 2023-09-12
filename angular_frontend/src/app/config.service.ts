import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  serverUrl!: string;
  serverPort!: string;

  constructor(private http: HttpClient) {}

	load() :Promise<any>  {

        const promise = this.http.get('/assets/config.json')
        .toPromise()
        .then(data => {
            console.log(data)
            Object.assign(this, data);
            return data;
        });

        return promise;
    }

}