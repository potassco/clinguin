import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ASPtranslateService {

  constructor() { }

  public toUserInputASP(node:string, id:string, type:string, name:string, value:string): string {
    return `user_input(${node},${id},${type},${name},${value})`
  }
  
}
