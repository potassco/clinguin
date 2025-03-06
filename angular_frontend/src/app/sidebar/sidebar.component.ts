import { ChangeDetectorRef, Component, Input, OnInit, ViewChild, ViewContainerRef, AfterViewInit } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { ChildBearerService } from '../child-bearer.service';

interface SidebarState {
  isPinned: boolean;
  position: 'start' | 'end';
  width: number;
}

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit, AfterViewInit {
  @ViewChild('childContainer', { read: ViewContainerRef }) childContainer!: ViewContainerRef;
  @Input() element: ElementDto | null = null;

  title: string = '';
  isPinned: boolean = false;
  isVisible: boolean = false;
  position: 'start' | 'end' = 'start';
  width: number = 300;

  private readonly STORAGE_KEY = 'sidebar_state';
  
  // Static cache for sidebar state
  private static stateCache: SidebarState | null = null;

  constructor(
    private cd: ChangeDetectorRef,
    private attributeService: AttributeHelperService,
    private elementLookupService: ElementLookupService,
    private childBearerService: ChildBearerService
  ) {}

  ngOnInit(): void {
    if (!this.element) return;
    
    this.elementLookupService.addElementObject(this.element.id, this, this.element);
    this.loadState();
  }

  ngAfterViewInit(): void {
    if (!this.element) return;
    
    this.setAttributes(this.element.attributes);

    requestAnimationFrame(() => {
      this.renderChildren();
      this.updateLayout();
    });
  }

  private renderChildren(): void {
    if (!this.element?.children?.length) return;
    
    this.element.children.forEach(childElement => {
      this.childBearerService.bearChild(this.childContainer, childElement, 'flex');
    });
  }

  private loadState(): void {
    try {
      // Check static cache first
      if (SidebarComponent.stateCache) {
        this.isPinned = SidebarComponent.stateCache.isPinned;
        this.isVisible = this.isPinned;
        this.position = SidebarComponent.stateCache.position;
        this.width = SidebarComponent.stateCache.width;
        return;
      }
      
      // Fall back to localStorage
      const savedState = localStorage.getItem(this.STORAGE_KEY);
      if (!savedState) return;
      
      const state = JSON.parse(savedState);
      
      this.isPinned = state.isPinned ?? false;
      this.isVisible = this.isPinned;
      this.position = state.position === 'start' || state.position === 'end' ? state.position : 'start';
      this.width = !isNaN(state.width) ? state.width : 300;
      
      // Update cache
      SidebarComponent.stateCache = {
        isPinned: this.isPinned,
        position: this.position,
        width: this.width
      };
    } catch (e) {
      console.error(`Failed to load sidebar state: ${e}`);
    }
  }

  private saveState(): void {
    try {
      // Update cache
      SidebarComponent.stateCache = {
        isPinned: this.isPinned,
        position: this.position,
        width: this.width
      };
      
      // Save to localStorage
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(SidebarComponent.stateCache));
    } catch (e) {
      console.error(`Failed to save sidebar state: ${e}`);
    }
  }

  setAttributes(attributes: AttributeDto[]): void {
    const title = this.attributeService.findGetAttributeValue("title", attributes, "");
    this.title = title;

    const position = this.attributeService.findGetAttributeValue("position", attributes, "start");
    if (position === "start" || position === "end") {
      this.position = position as "start" | "end";
    }

    const widthStr = this.attributeService.findGetAttributeValue("width", attributes, "300");
    const width = parseInt(widthStr, 10);
    if (!isNaN(width)) {
      this.width = width;
    }

    const sidebarElement = document.querySelector('.offcanvas-sidebar') as HTMLElement;
    if (sidebarElement) {
      this.attributeService.addClasses(sidebarElement, attributes, [], []);
    }

    document.documentElement.style.setProperty('--sidebar-width', `${this.width}px`);
  }

  toggle(): void {
    this.isPinned = !this.isPinned;
    this.isVisible = true;

    this.saveState();
    this.updateLayout();
  }

  show(): void {
    if (!this.isPinned) {
      this.isVisible = true;
      this.cd.detectChanges();
    }
  }

  hideOnMouseLeave(event: MouseEvent): void {
    if (!this.isPinned) {
      this.isVisible = false;
      this.cd.detectChanges();
    }
  }

  private updateLayout(): void {
    const navbar = document.querySelector('.navbar') as HTMLElement;
    const contentWrapper = document.querySelector('.content-wrapper') as HTMLElement;
    const sidebarElement = document.querySelector('.offcanvas-sidebar') as HTMLElement;

    if (!navbar || !contentWrapper || !sidebarElement) return;
    
    const navbarHeight = navbar.offsetHeight;

    if (this.isPinned) {
      this.updatePinnedLayout(sidebarElement, navbar, contentWrapper, navbarHeight);
    } else {
      this.updateUnpinnedLayout(sidebarElement, navbar, contentWrapper, navbarHeight);
    }

    this.cd.detectChanges();
  }
  
  private updatePinnedLayout(
    sidebarElement: HTMLElement, 
    navbar: HTMLElement, 
    contentWrapper: HTMLElement, 
    navbarHeight: number
  ): void {
    // Position sidebar below navbar
    sidebarElement.style.top = `${navbarHeight}px`;
    sidebarElement.style.height = `calc(100vh - ${navbarHeight}px)`;

    document.body.classList.add('has-sidebar-pinned');
    document.body.classList.add(`sidebar-position-${this.position}`);

    // Adjust layout based on position
    if (this.position === 'start') {
      contentWrapper.style.marginLeft = `${this.width}px`;
      navbar.style.paddingLeft = `${this.width}px`;
    } else {
      contentWrapper.style.marginRight = `${this.width}px`;
      navbar.style.paddingRight = `${this.width}px`;
    }

    contentWrapper.style.paddingTop = `${navbarHeight}px`;
  }
  
  private updateUnpinnedLayout(
    sidebarElement: HTMLElement, 
    navbar: HTMLElement, 
    contentWrapper: HTMLElement, 
    navbarHeight: number
  ): void {
    sidebarElement.style.top = '10vh';
    sidebarElement.style.height = '80vh';

    // Remove body classes
    document.body.classList.remove('has-sidebar-pinned');
    document.body.classList.remove('sidebar-position-start');
    document.body.classList.remove('sidebar-position-end');

    // Reset margins and padding
    navbar.style.paddingLeft = '';
    navbar.style.paddingRight = '';
    contentWrapper.style.marginLeft = '';
    contentWrapper.style.marginRight = '';
    contentWrapper.style.paddingTop = `${navbarHeight}px`;
  }
}