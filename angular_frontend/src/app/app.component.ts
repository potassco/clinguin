import { ChangeDetectorRef, Component, ElementRef, ViewChild } from '@angular/core';
import { DrawFrontendService } from './draw-frontend.service';
import { ElementDto } from './types/json-response.dto';
import { ElementLookupDto, ElementLookupService } from './element-lookup.service';
import { LocatorService } from './locator.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  @ViewChild('contentWrapper',{static:false}) contentWrapper!: ElementRef;

  title = 'Clinguin';

  menuBar : ElementDto | null = null
  messageList : ElementDto[] = []

  constructor(private frontendService: DrawFrontendService, private cd: ChangeDetectorRef, private elementLookupService: ElementLookupService) {}


  ngAfterViewInit(): void {

    this.frontendService.menuBar.subscribe({next: data => {
      // Explicitly set to null and then to data (again), as otherwise typescript doesn't get it that a change occurred...
      this.menuBar = null
      this.cd.detectChanges()
      this.menuBar = data
      this.cd.detectChanges()
    }})

    this.contentWrapper.nativeElement.addEventListener("click", function(){
      console.log("CLICK SOMEWHERE")

      let lookupService = LocatorService.injector.get(ElementLookupService)

      lookupService.elementLookup.forEach((element:ElementLookupDto) => {
        if (element.element.type == "menu_bar_section" && element.object != null && "collapsed" in element.object) {
            console.log("42")
            if (element.object.collapsed == false) {
              console.log("44")
              element.object.collapsed = true
            }
          }         
      })
    })

  }
}
