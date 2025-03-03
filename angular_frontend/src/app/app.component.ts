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
	sidebarVisible: boolean = false;

	menuBar : ElementDto | null = null
	messageList : ElementDto[] = []

	constructor(private frontendService: DrawFrontendService, private cd: ChangeDetectorRef, private elementLookupService: ElementLookupService) {}


	ngAfterViewInit(): void {

		this.frontendService.menuBar.subscribe({next: data => {
			this.menuBar = null
			this.cd.detectChanges()
			this.menuBar = data
			this.cd.detectChanges()
		}})

		this.contentWrapper.nativeElement.addEventListener("click", function(){
			let lookupService = LocatorService.injector.get(ElementLookupService)

			lookupService.elementLookup.forEach((element:ElementLookupDto) => {
				if (element.element.type == "menu_bar_section" && element.object != null && "collapsed" in element.object) {
					if (element.object.collapsed == false) {
						element.object.collapsed = true
					}
				}
			})
		})
  	}
}
