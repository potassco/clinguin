import { Injectable } from "@angular/core";
import { NgbModalRef } from "@ng-bootstrap/ng-bootstrap";

@Injectable({
  providedIn: 'root'
})
export class ModalRefService {

    modals: {key:string,modalRef:NgbModalRef}[] = []

    registerModal(key:string, modalRef: NgbModalRef) : void {
        this.modals.push({key:key, modalRef: modalRef})
    }

    removeModalByKey(key:string) : number {

        let foundIndex = -1
        for (let index = 0; index < this.modals.length; index++) {
            let item = this.modals[index]
            if (item.key == key) {
                foundIndex = index
                break
            }
        }
       
        if (foundIndex >= 0) {
            delete this.modals[foundIndex]
        }

        return foundIndex
    }

    closeRemoveAllModals() : void {
        this.modals.forEach((item:{key:string, modalRef:NgbModalRef}) => {
            item.modalRef.close()
        })

        this.modals.length = 0
    }

}