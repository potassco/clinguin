import { ChangeDetectorRef, Component, ElementRef, ViewChild, ViewContainerRef } from '@angular/core';
import { HttpService } from 'src/app/http.service';
import { ElementDto } from 'src/app/types/json-response.dto';
import { ComponentResolutionService } from 'src/app/component-resolution.service';
import { AttributeHelperService } from 'src/app/attribute-helper.service';

@Component({
  selector: 'app-new-main',
  templateUrl: './window.component.html',
  styleUrls: ['./window.component.scss']
})
export class WindowComponent {
  @ViewChild('parent',{static:false}) parent!: ElementRef;
  @ViewChild('child',{read: ViewContainerRef}) child!: ViewContainerRef;

  children: any = []

  window_id: string = ""
  window: ElementDto | null = null
  
  constructor(private httpService: HttpService, private cd: ChangeDetectorRef) {
  }

  ngAfterViewInit(): void {


    this.httpService.get().subscribe(
      {next: (data:ElementDto) => {
        console.log(data)

        
        let window = data.children[0]

        this.window_id = window.id

        this.window = window

        this.cd.detectChanges()

        window.children.forEach(item => {


          let my_comp = ComponentResolutionService.component_resolution(this.child, item.type)

          if (my_comp != null) {
            //my_comp.instance.element = item
            my_comp.setInput("element",item)
            let html: HTMLElement = <HTMLElement>my_comp.location.nativeElement
            html.id = item.id

            AttributeHelperService.add_attributes(html, item.attributes)


            this.children.push(my_comp)

          }
        })

        let parent_html = this.parent.nativeElement
        AttributeHelperService.add_attributes(parent_html, window.attributes)

        this.cd.detectChanges()
        // Prevents Errors
      },
      error: (err) => console.log(err)}
    )

    
  }



}
