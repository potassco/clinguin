import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CallbackDto, ElementDto } from '../types/json-response.dto';
import { HttpService } from '../http.service';

@Component({
  selector: 'app-dropdown-menu',
  templateUrl: './dropdown-menu.component.html',
  styleUrls: ['./dropdown-menu.component.scss']
})
export class DropdownMenuComponent {
  // Why does the dropdown need this?
  @Input() element : ElementDto | null = null

  buttonLabel : string = ""
  dropDownMenuItems : {label:string, element:ElementDto}[] = []

  constructor(private  cd: ChangeDetectorRef, private httpService : HttpService) {
  }


  ngAfterViewInit(): void {

    if (this.element != null) {
      let index = this.element.attributes.findIndex(attr => attr.key == "label")
      if (index >= 0) {
        this.buttonLabel = this.element.attributes[index].value
      }

      this.element.children.forEach(child => {
        let index = child.attributes.findIndex(attr => attr.key == "label")
        if (index >= 0) {
          this.dropDownMenuItems.push({label:child.attributes[index].value, element:child})
        }
      })
    }

    this.cd.detectChanges()
  }

  onClick(element: ElementDto) {

    let callback : CallbackDto = element.callbacks[0]

    this.httpService.post(callback.policy).subscribe(
      {next: (data:ElementDto) => console.log(data)})
    /*
      TODO -> Continue here
      -> Implement basic callback functionality, etc.
    */
  }
}
