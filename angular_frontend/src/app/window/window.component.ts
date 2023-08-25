import { ChangeDetectorRef, Component, ComponentRef, ElementRef, ViewChild, ViewContainerRef } from '@angular/core';
import { HttpService } from 'src/app/http.service';
import { ElementDto } from 'src/app/types/json-response.dto';
import { ComponentResolutionService } from 'src/app/component-resolution.service';
import { AttributeHelperService } from 'src/app/attribute-helper.service';
import { DrawFrontendService } from '../draw-frontend.service';
import { ContainerComponent } from '../container/container.component';
import { DropdownMenuComponent } from '../dropdown-menu/dropdown-menu.component';

@Component({
  selector: 'app-new-main',
  templateUrl: './window.component.html',
  styleUrls: ['./window.component.scss']
})
export class WindowComponent {
  @ViewChild('parent',{static:false}) parent!: ElementRef;
  @ViewChild('child',{read: ViewContainerRef}) child!: ViewContainerRef;

  children: ComponentRef<any>[] = []

  window_id: string = ""
  window: ElementDto | null = null

  menuBar: ElementDto | null = null
  
  constructor(private httpService: HttpService, private cd: ChangeDetectorRef, private frontendService: DrawFrontendService) {
  }

  ngAfterViewInit(): void {

    this.frontendService.initialGet()


    this.frontendService.frontendJson.subscribe({next: (data:ElementDto) => {

        this.children.forEach(child => {
          this.child.clear()
        })
        this.children = []

        this.cleanValues(data)
 
        let window = data.children[0]

        this.window_id = window.id

        this.window = window

        this.cd.detectChanges()

        window.children.forEach(item => {


          let my_comp = ComponentResolutionService.componentCreation(this.child, item.type)

          if (my_comp != null) {
            my_comp.setInput("element",item)
            let html: HTMLElement = <HTMLElement>my_comp.location.nativeElement
            html.id = item.id

            AttributeHelperService.addAttributes(html, item.attributes)

            this.children.push(my_comp)
          }
        })

        let parent_html = this.parent.nativeElement
        AttributeHelperService.addAttributes(parent_html, window.attributes)

        // Prevents Errors
        this.cd.detectChanges()
      },
      error: (err) => console.log(err)})
  }

  cleanValues(element: ElementDto) {
    for (let i = 0; i < element.attributes.length; i++) {
      let value = element.attributes[i].value
      value = this.stringSanitizer(value)
      element.attributes[i].value = value

      let key = element.attributes[i].key
      key = this.stringSanitizer(key)
      element.attributes[i].key = key
    }

    for (let i = 0; i < element.callbacks.length; i++) {
      let policy = element.callbacks[i].policy
      policy = this.stringSanitizer(policy)
      element.callbacks[i].policy = policy

      let action = element.callbacks[i].action
      action = this.stringSanitizer(action)
      element.callbacks[i].action = action
    }

    element.children.forEach(child => {
      this.cleanValues(child)
    })
  }

  stringSanitizer(value:string) : string {
    if (value.length > 0) {
      if (value[0] == '"') {
        value = value.slice(1)
      }
    }

    if (value.length > 0) {
      if (value[value.length - 1] == '"') {
        value = value.slice(0, -1)
      }
    }

    value = value.replace("\\n","<br>")

    return value
  }

}
