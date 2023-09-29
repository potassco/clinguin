import { ChangeDetectorRef, Component, ComponentRef, ElementRef, Input, TemplateRef, ViewChild, ViewContainerRef } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { ChildBearerService } from '../child-bearer.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { ModalDismissReasons, NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { ModalRefService } from '../modal-ref.service';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent {
  @ViewChild('child',{read: ViewContainerRef}) child!: ViewContainerRef;
  @ViewChild('content',{read: TemplateRef}) content!: TemplateRef<any>;

  @Input() element: ElementDto | null = null
  @Input() parentLayout: string = ""

  container_id: string = ""
  container: ElementDto | null = null
  modalTitle: string = ""

  modalRef : NgbModalRef | null = null

  closeResult = '';
  
  constructor(private childBearerService: ChildBearerService, private cd: ChangeDetectorRef, private attributeService: AttributeHelperService, private elementLookupService: ElementLookupService, private modalService: NgbModal, private modalRefService: ModalRefService) {
  }

  ngAfterViewInit(): void {

    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element)

      this.setAttributes(this.element.attributes)


      this.cd.detectChanges()
    }
  }

  setAttributes(attributes: AttributeDto[]) {

    let visibility = this.attributeService.findAttribute("visible", attributes)

    let modalTitle = this.attributeService.findAttribute("title", attributes)
    if (modalTitle != null) {
      this.modalTitle = modalTitle.value
    }

    if (visibility != null && this.element != null) {

      if ((visibility.value == "shown" || visibility.value == "visible") && (this.modalRef == null)) {
    
        this.modalRef = this.modalService.open(this.content, { ariaLabelledBy: 'modal-basic-title' })

        this.modalRefService.registerModal(this.element.id, this.modalRef)

        this.modalRef.result.then(
          (result) => {
            this.closeResult = `Closed with: ${result}`;
            console.log(this.closeResult)

            if (this.element != null) {
              for (let index = 0; index < this.element.attributes.length; index++) {
                let attribute = this.element.attributes[index]
                if (attribute.key == "shown" || attribute.key == "visible") {
                  attribute.value = "hidden"
                }
              }
            }

            this.modalRef = null
          },
          (reason) => {
            this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
            console.log(this.closeResult)
            
            if (this.element != null) {
              for (let index = 0; index < this.element.attributes.length; index++) {
                let attribute = this.element.attributes[index]
                if (attribute.key == "shown" || attribute.key == "visible") {
                  attribute.value = "hidden"
                }
              }
            }

            if (this.element != null) {
              this.modalRefService.removeModalByKey(this.element.id)
            }
            
            this.modalRef = null
          },
        );  
      } else if (this.modalRef != null && (visibility.value == "hidden" || visibility.value == "collapse")) {
        this.modalRef.close()
      }

      this.cd.detectChanges()
    }
  }

	private getDismissReason(reason: any): string {
		if (reason === ModalDismissReasons.ESC) {
			return 'by pressing ESC';
		} else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
			return 'by clicking on a backdrop';
		} else {
			return `with: ${reason}`;
		}
	}


}
