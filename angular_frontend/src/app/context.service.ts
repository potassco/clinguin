import { Injectable } from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class ContextService {

    contextKeyVal: ContextItem[] = []

    addContext(key: string, value: any) {
        let found = false
        for (let index = 0; index < this.contextKeyVal.length; index++) {
            let item = this.contextKeyVal[index]
            if (item.key == key) {
                item.value = value
                found = true
            }
        }

        if (!found) {
            this.contextKeyVal.push(new ContextItem(key, value))
        }
    }

    getContext(): ContextItem[] {
        return this.contextKeyVal
    }

    retrieveContextValue(key: string): string {

        let foundIndex = -1
        for (let index = 0; index < this.contextKeyVal.length; index++) {
            if (this.contextKeyVal[index].key == key) {
                foundIndex = index
                break
            }
        }

        if (foundIndex >= 0) {
            return this.contextKeyVal[foundIndex].value
        } else {
            return ""
        }
    }

    clearContext(): void {
        this.contextKeyVal.length = 0
    }
}

export class ContextItem {
    key!: string
    value!: string

    constructor(key: string, value: string) {
        this.key = key
        this.value = value
    }
}

