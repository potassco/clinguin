import { Injectable } from "@angular/core";
import { NgbModalRef } from "@ng-bootstrap/ng-bootstrap";
import { ElementDto } from "./types/json-response.dto";
import { DrawFrontendService } from "./draw-frontend.service";

@Injectable({
  providedIn: 'root'
})
export class ContextMenuService {

    constructor() {

    }


    contextMenus: {key:string,contextMenu:ElementDto}[] = []

    registerContextMenu(key:string, contextMenu: ElementDto) : void {
        this.contextMenus.push({key:key, contextMenu: contextMenu})
    }

    removeContextMenuByKey(key:string) : number {

        let foundIndex = -1
        for (let index = 0; index < this.contextMenus.length; index++) {
            let item = this.contextMenus[index]
            if (item.key == key) {
                foundIndex = index
                break
            }
        }
       
        if (foundIndex >= 0) {
            delete this.contextMenus[foundIndex]
        }

        return foundIndex
    }

    retrieveContextValue(key: string): ElementDto | null {

        let foundIndex = -1
        for (let index = 0; index < this.contextMenus.length; index++) {
            if (this.contextMenus[index].key == key) {
                foundIndex = index
                break
            }
        }

        if (foundIndex >= 0) {
            return this.contextMenus[foundIndex].contextMenu
        } else {
            return null
        }
    }

    removeAllContextMenus() : void {
        this.contextMenus.length = 0
    }

}