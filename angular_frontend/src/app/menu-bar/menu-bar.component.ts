import { ChangeDetectorRef, Component, Input, ElementRef, ViewChild, AfterViewInit, OnDestroy, HostListener } from '@angular/core';
import { AttributeDto, WhenDto, ElementDto } from '../types/json-response.dto';
import { DrawFrontendService } from '../draw-frontend.service';
import { AttributeHelperService } from '../attribute-helper.service';
import { CallBackHelperService } from '../callback-helper.service';
import { ElementLookupService } from '../element-lookup.service';

@Component({
	selector: 'app-menu-bar',
	templateUrl: './menu-bar.component.html',
	styleUrls: ['./menu-bar.component.scss']
})
export class MenuBarComponent implements AfterViewInit, OnDestroy {
	@Input() element: ElementDto | null = null;
	@ViewChild("titleIcon", { static: false }) titleIcon!: ElementRef;
	@ViewChild("navbarElement", { static: false }) navbarElement!: ElementRef;

	public isCollapsed = true;
	private resizeTimeout: any;

	title: string = "";
	menuBarButtons: MenuBarButton[] = [];

	constructor(
		private cd: ChangeDetectorRef, 
		private displayFrontend: DrawFrontendService, 
		private callbackService: CallBackHelperService,
		private attributeService: AttributeHelperService, 
		private elementLookupService: ElementLookupService
	) {}

	ngAfterViewInit(): void {
		if (!this.element) return;
		
		this.elementLookupService.addElementObject(this.element.id, this, this.element);
		this.initializeButtons();
		this.setAttributes(this.element.attributes);
		
		setTimeout(() => this.updateLayout(), 100);
	}
	
	ngOnDestroy(): void {
		clearTimeout(this.resizeTimeout);
	}

	@HostListener('window:resize')
	onResize() {
		clearTimeout(this.resizeTimeout);
		this.resizeTimeout = setTimeout(() => this.updateLayout(), 100);
	}

	private initializeButtons(): void {
		if (!this.element) return;
		
		this.element.children.forEach(childElement => {
			const label = this.attributeService.findGetAttributeValue("label", childElement.attributes, "");
			const order = parseInt(this.attributeService.findGetAttributeValue("order", childElement.attributes, "0"));
			const button = new MenuBarButton(childElement.id, label, childElement, order);
			this.elementLookupService.addElementObject(childElement.id, button, childElement);
			this.menuBarButtons.push(button);
		});

		this.menuBarButtons.sort((a, b) => a.order - b.order);
		this.cd.detectChanges();

		this.menuBarButtons.forEach(button => {
			const btnElement = document.getElementById(button.id);
			if (btnElement) {
				button.setHtmlElement(btnElement);
				this.attributeService.addClasses(btnElement, button.element.attributes, 
					["btn-sm", "mx-1"], ["btn-outline-dark", "border-0"]);
				this.callbackService.setCallbacks(btnElement, button.element.when);
				
				const icon = btnElement.children.item(0);
				if (icon) {
					this.attributeService.addClasses(icon, button.element.attributes, ["fa"], [], 'icon');
				}
			}
		});
	}

	private updateLayout(): void {
		if (!this.navbarElement) return;
		
		const navbarHeight = this.navbarElement.nativeElement.offsetHeight;
		document.documentElement.style.setProperty('--navbar-height', `${navbarHeight}px`);
		
		const contentWrapper = document.querySelector('.content-wrapper') as HTMLElement;
		if (contentWrapper) {
			contentWrapper.style.paddingTop = `${navbarHeight}px`;
		}

		const isMobile = window.innerWidth < 768;
		if (isMobile) {
			this.isCollapsed = true;
		}

		this.cd.detectChanges();
	}

	adjustForSidebar(position: string, width: number): void {
		const navbar = this.navbarElement?.nativeElement;
		if (!navbar) return;

		const isMobile = window.innerWidth < 768;
		const adjustedWidth = isMobile ? Math.min(width, 60) : width;

		if (position === 'start') {
			navbar.style.paddingLeft = `${adjustedWidth}px`;
			navbar.style.paddingRight = '';
		} else {
			navbar.style.paddingRight = `${adjustedWidth}px`;
			navbar.style.paddingLeft = '';
		}
	}

	resetSidebarAdjustments(): void {
		const navbar = this.navbarElement?.nativeElement;
		if (navbar) {
			navbar.style.paddingLeft = '';
			navbar.style.paddingRight = '';
		}
	}

	setAttributes(attributes: AttributeDto[]): void {
		const titleAttribute = this.attributeService.findAttribute("title", attributes);
		if (titleAttribute) {
			this.title = titleAttribute.value;
		}
		
		if (this.titleIcon) {
			this.attributeService.addClasses(this.titleIcon.nativeElement, attributes, ["fa"], [], 'icon');
		}
		
		this.cd.detectChanges();
	}

	operationExecutor(operation: WhenDto | null): void {
		if (operation) {
			this.displayFrontend.operationPost(operation);
		}
	}
}

class MenuBarButton {
	id: string;
	title: string;
	element: ElementDto;
	order: number;
	htmlElement: HTMLElement | null = null;

	constructor(id: string, title: string, element: ElementDto, order: number) {
		this.id = id;
		this.title = title;
		this.element = element;
		this.order = order;
	}

	setHtmlElement(htmlElement: HTMLElement): void {
		this.htmlElement = htmlElement;
	}
}