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
	@Input() isFixed: boolean = true;

	public isCollapsed = true;
	private resizeTimeout: any;
	private resizeObserver: ResizeObserver | null = null;

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
		
		this.initializeElement();
		this.initializeMenuBarButtons();
		this.applyGlobalAttributes();
		this.initializeResizeObserver();

		setTimeout(() => {
			this.updateContentPadding();
		}, 100);
	}
	
	ngOnDestroy(): void {
		this.resizeObserver?.disconnect();
	}

	@HostListener('window:resize')
	onResize() {
		clearTimeout(this.resizeTimeout);
		this.resizeTimeout = setTimeout(() => {
			this.updateContentPadding();
		}, 100);
	}

	private initializeElement(): void {
		if (this.element) {
			this.elementLookupService.addElementObject(this.element.id, this, this.element);
		}
	}

	private initializeMenuBarButtons(): void {
		if (!this.element) return;
		
		this.element.children.forEach(childElement => {
			const label = this.attributeService.findGetAttributeValue("label", childElement.attributes, "");
			const order = this.attributeService.findGetAttributeValue("order", childElement.attributes, "0");
			const button = new MenuBarButton(childElement.id, label, childElement, order);
			this.elementLookupService.addElementObject(childElement.id, button, childElement);
			this.menuBarButtons.push(button);
		});

		this.cd.detectChanges();

		this.menuBarButtons.sort((a, b) => a.order - b.order);

		this.menuBarButtons.forEach(button => {
		const btnElement = document.getElementById(button.id);
			if (btnElement) {
				button.setHtmlElement(btnElement);
				button.setAttributes(button.element.attributes);
				this.attributeService.addClasses(btnElement, button.element.attributes, ["btn-sm", "mx-1"], ["btn-outline-dark", "border-0"]);
				this.callbackService.setCallbacks(btnElement, button.element.when);
				const icon = btnElement.children.item(0);
				if (icon) {
					this.attributeService.addClasses(icon, button.element.attributes, ["fa"], [], 'icon');
				}
			}
		});
	}

	private applyGlobalAttributes(): void {
		if (!this.element) return;
		this.setAttributes(this.element.attributes);
		this.cd.detectChanges();
	}

	private initializeResizeObserver(): void {
		if (this.navbarElement && window.ResizeObserver) {
			this.resizeObserver = new ResizeObserver(() => {
				this.updateNavbarHeight();
			});
			this.resizeObserver.observe(this.navbarElement.nativeElement);
		}
	}

	updateContentPadding(): void {
		if (!this.navbarElement) return;
		const navbarHeight = this.navbarElement.nativeElement.offsetHeight;
		this.updateCssProperties(navbarHeight);
		this.cd.detectChanges();
	}

	updateNavbarHeight(): void {
		if (!this.navbarElement) return;
		const height = this.navbarElement.nativeElement.offsetHeight;
		this.updateCssProperties(height);
	}

	private updateCssProperties(navbarHeight: number): void {
		document.documentElement.style.setProperty('--navbar-height', `${navbarHeight}px`);
		
		const contentWrapper = document.querySelector('.content-wrapper') as HTMLElement;
		if (contentWrapper) {
			contentWrapper.style.paddingTop = `${navbarHeight}px`;
		}
		
		const pinnedOffcanvas = document.querySelector('.offcanvas-sidebar.pinned') as HTMLElement;
		if (pinnedOffcanvas) {
			pinnedOffcanvas.style.top = `${navbarHeight}px`;
			pinnedOffcanvas.style.height = `calc(100vh - ${navbarHeight}px)`;
		}
	}
	
	adjustForSidebar(position: string, width: number): void {
		if (this.titleIcon && this.titleIcon.nativeElement) {
			const navbar = this.titleIcon.nativeElement.closest('.navbar') as HTMLElement;
			if (navbar) {
				if (position === 'start') {
				navbar.style.paddingLeft = `${width}px`;
				} else if (position === 'end') {
				navbar.style.paddingRight = `${width}px`;
				}
			}
		}
	}
	
	resetSidebarAdjustments(): void {
		if (this.titleIcon && this.titleIcon.nativeElement) {
			const navbar = this.titleIcon.nativeElement.closest('.navbar') as HTMLElement;
			if (navbar) {
				navbar.style.paddingLeft = '';
				navbar.style.paddingRight = '';
			}
		}
	}

	setAttributes(attributes: AttributeDto[]): void {
		const titleAttribute = this.attributeService.findAttribute("title", attributes);
		if (titleAttribute) {
			this.title = titleAttribute.value;
		}
		const iconHtml = this.titleIcon.nativeElement;
		this.attributeService.addClasses(iconHtml, attributes, ["fa"], [], 'icon');
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

	constructor(id: string, title: string, element: ElementDto, order: string | null) {
		this.id = id;
		this.title = title;
		this.element = element;
		this.order = order ? parseInt(order) : 0;
	}

	setHtmlElement(htmlElement: HTMLElement): void {
		this.htmlElement = htmlElement;
	}

	setAttributes(attributes: AttributeDto[]): void {
		const labelAttribute = attributes.find(item => item.key === "label");
		this.title = labelAttribute ? labelAttribute.value : "";
	}
}

class MenuBarItem {
	id: string;
	title: string;
	element: ElementDto;
	htmlElement: HTMLElement | null = null;

	constructor(id: string, title: string, element: ElementDto) {
		this.id = id;
		this.title = title;
		this.element = element;
	}

	setHtmlElement(htmlElement: HTMLElement): void {
		this.htmlElement = htmlElement;
	}

	setAttributes(attributes: AttributeDto[]): void {
		const labelAttribute = attributes.find(item => item.key === "label");
		this.title = labelAttribute ? labelAttribute.value : "";
	}
}

class MenuBarSection {
	id: string = "menuBarSection";
	title: string = "";
	element: ElementDto;
	menuBarItems: MenuBarItem[];
	collapsed: boolean = true;
	htmlElement: HTMLElement | null = null;

	constructor(id: string, title: string, menuBarItems: MenuBarItem[], element: ElementDto) {
		this.id = id;
		this.title = title;
		this.menuBarItems = menuBarItems;
		this.element = element;
	}

	toggleCollapsed(): void {
		this.collapsed = !this.collapsed;
	}

	setHtmlElement(htmlElement: HTMLElement): void {
		this.htmlElement = htmlElement;
	}

	setAttributes(attributes: AttributeDto[]): void {
		const labelAttribute = attributes.find(item => item.key === "label");
		this.title = labelAttribute ? labelAttribute.value : "";
	}
}