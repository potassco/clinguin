import { Injectable } from "@angular/core";

@Injectable({
  providedIn: 'root'
})
export class ContextService {

    contextKeyVal : {"key":string, "val":string}[] = []

    addContext(key: string, val: string) {
        this.contextKeyVal.push({"key":key, "val":val})
    }

    getContext() : {"key":string, "val":string}[] {
        return this.contextKeyVal
    }
}

