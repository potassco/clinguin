import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild, ViewContainerRef, OnInit, AfterViewInit } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { ChildBearerService } from '../child-bearer.service';
import { CallBackHelperService } from '../callback-helper.service';

interface TabItem {
  id: string;
  title: string;
  element: ElementDto;
  container?: HTMLElement;
  order: number;
}

@Component({
  selector: 'app-tabs',
  templateUrl: './tabs.component.html',
  styleUrls: ['./tabs.component.scss']
})
export class TabsComponent implements OnInit, AfterViewInit {
  @ViewChild('tabContent', { read: ViewContainerRef, static: false }) tabContent!: ViewContainerRef;
  @ViewChild('tabNav', { static: false }) tabNav!: ElementRef;
  @ViewChild('tabContentWrapper', { static: false }) tabContentWrapper!: ElementRef;
  @ViewChild('tabsContainer', { static: false }) tabsContainer!: ElementRef;

  @Input() element: ElementDto | null = null;

  tabs: TabItem[] = [];
  activeTabId: string = '';
  contentRendered: boolean = false;
  orientation: string = 'horizontal';
  navClasses: string[] = ['nav-pills', 'nav-fill'];

  private readonly STORAGE_KEY_PREFIX = 'tabs_state_';

  constructor(
    private cd: ChangeDetectorRef,
    private attributeService: AttributeHelperService,
    private elementLookupService: ElementLookupService,
    private childBearerService: ChildBearerService,
    private callbackService: CallBackHelperService
  ) {}

  ngOnInit(): void {
    if (this.element) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element);
    }
  }

  ngAfterViewInit(): void {
    if (!this.element) return;
    this.processTabItems();
    this.loadTabState();
    this.setAttributes(this.element.attributes);
    if (this.element.when?.length) {
      const tagHtml = this.elementLookupService.getElement(this.element.id)?.tagHtml;
      if (tagHtml) {
        this.callbackService.setCallbacks(tagHtml, this.element.when);
      }
    }
    requestAnimationFrame(() => {
      this.renderContent();
    });
  }

  private processTabItems(): void {
    if (!this.element?.children) return;
    const tabItems = this.element.children.filter(child => child.type === 'tabs_item');
    this.tabs = tabItems.map(tabElement => ({
      id: tabElement.id,
      title: this.attributeService.findGetAttributeValue("title", tabElement.attributes, "Tab"),
      element: tabElement,
      order: parseInt(this.attributeService.findGetAttributeValue("order", tabElement.attributes, "0"), 10) || 0
    })).sort((a, b) => a.order - b.order);
    this.cd.detectChanges();
  }

  private loadTabState(): void {
    try {
      const savedState = localStorage.getItem(this.STORAGE_KEY_PREFIX + (this.element?.id || 'default'));
      if (savedState) {
        const state = JSON.parse(savedState);
        if (state.activeTabId && this.tabs.some(tab => tab.id === state.activeTabId)) {
          this.activeTabId = state.activeTabId;
        }
      }
    } catch (e) {
      console.error(`Failed to load tab state: ${e}`);
    }
  }

  private saveTabState(): void {
    try {
      localStorage.setItem(
        this.STORAGE_KEY_PREFIX + (this.element?.id || 'default'),
        JSON.stringify({ activeTabId: this.activeTabId })
      );
    } catch (e) {
      console.error(`Failed to save tab state: ${e}`);
    }
  }

  setAttributes(attributes: AttributeDto[]): void {
	this.orientation = this.attributeService.findGetAttributeValue("orientation", attributes, "horizontal");
	const classAttrValues = this.attributeService.findAttributeList("class", attributes);
	const classAttrValue = classAttrValues.join(' ');
	const useNavFill = classAttrValue.indexOf("nav-fill") > -1;
	let navType = "nav-tabs";
	if (classAttrValue.indexOf("nav-pills") > -1) {
	navType = "nav-pills";
	}
	this.navClasses = [navType];
	if (useNavFill) {
	this.navClasses.push("nav-fill");
	}
	if (this.tabsContainer) {
	  const container = this.tabsContainer.nativeElement;
	  container.style.display = 'flex';
	  if (this.orientation === 'vertical') {
		container.style.flexDirection = 'row';
		container.style.alignItems = 'stretch';
	  } else {
		container.style.flexDirection = 'column';
		container.style.alignItems = 'flex-start';
	  }
	  this.attributeService.setAttributesDirectly(container, attributes);
	  this.attributeService.addAttributes(container, attributes);
	  this.attributeService.addGeneralAttributes(container, attributes);
	}
	if (this.tabNav) {
	  const navElement = this.tabNav.nativeElement;
	  navElement.style.display = 'flex';
	  navElement.style.flexDirection = this.orientation === 'vertical' ? 'column' : 'row';
	  navElement.style.flexShrink = '0';
	  if (this.orientation === 'vertical' && useNavFill) {
		navElement.style.height = '100%';
	  }
	  if (this.orientation === 'horizontal' && useNavFill) {
		navElement.style.width = '100%';
	  }
	  navElement.className = ['nav', ...this.navClasses].join(' ');
	  this.attributeService.addClasses(navElement, attributes, [], []);
	}
	if (this.tabContentWrapper) {
	  const contentEl = this.tabContentWrapper.nativeElement;
	  contentEl.style.flex = '';
	  contentEl.style.minHeight = '';
	  if (this.orientation === 'vertical') {
		contentEl.style.flex = '1 1 auto';
	  }
	  contentEl.className = 'tab-content';
	}
	this.applyTabButtonStyling();
	this.cd.detectChanges();
  }

  renderContent(): void {
    if (!this.tabContent || this.contentRendered) return;
    this.contentRendered = true;
    this.tabContent.clear();
    this.tabs.forEach(tab => {
      const container = document.createElement('div');
      container.className = 'tab-pane';
      container.style.display = this.isTabActive(tab.id) ? 'block' : 'none';
      container.setAttribute('data-tab-id', tab.id);
      this.tabContent.element.nativeElement.appendChild(container);
      tab.container = container;
      if (tab.element.children?.length) {
        tab.element.children.forEach(childElement => {
          const componentRef = this.childBearerService.bearChild(this.tabContent, childElement, 'flex');
          if (componentRef) {
            container.appendChild(componentRef.location.nativeElement);
          }
        });
      }
    });
    this.cd.detectChanges();
  }

  isTabActive(tabId: string): boolean {
    return this.activeTabId === tabId;
  }

  setActiveTab(tabId: string): void {
    this.activeTabId = (this.activeTabId === tabId) ? '' : tabId;
    this.tabs.forEach(tab => {
      if (!tab.container) return;
      tab.container.style.display = this.isTabActive(tab.id) ? 'block' : 'none';
    });
    this.applyTabButtonStyling();
    this.saveTabState();
    this.cd.detectChanges();
  }

  private applyTabButtonStyling(): void {
    this.tabs.forEach(tab => {
      const btn = document.getElementById(`tab-btn-${tab.id}`);
      if (!btn) return;
      let newClasses = ["nav-link"];
      const attrKey = this.isTabActive(tab.id) ? "active_class" : "inactive_class";
      const customClassValues = this.attributeService.findAttributeList(attrKey, tab.element.attributes);
      let customClasses: string[] = [];
      customClassValues.forEach(value => {
        const cleaned = value.replace(/[\(\)"]/g, '').trim();
        customClasses.push(...cleaned.split(';').map(c => c.trim()).filter(Boolean));
      });
      newClasses.push(...customClasses);
      btn.className = newClasses.join(" ");
    });
  }
}