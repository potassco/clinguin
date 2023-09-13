import { Injectable } from "@angular/core";

@Injectable({
  providedIn: 'root'
})
export class ContextService {

    contextKeyVal : ContextItem[] = []

    addContext(key: string, val: string) {

        let found = false
        for (let index = 0; index < this.contextKeyVal.length; index++) {
            let item = this.contextKeyVal[index]
            if (item.key == key) {
                item.value = val
                found = true
            }
        }

        if (found == false) {
            this.contextKeyVal.push(new ContextItem(key, val))
        }
    }

    getContext() : ContextItem[] {
        return this.contextKeyVal
    }
}

export class ContextItem {
    key!:string
    value!:string

    constructor(key:string, value:string) {
        this.key = key
        this.value = value
    }
}

