import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild, ViewContainerRef, OnInit, Optional } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { ChildBearerService } from '../child-bearer.service';

@Component({
  selector: 'app-collapse',
  templateUrl: './collapse.component.html'
})
export class CollapseComponent implements OnInit {
  @ViewChild('toggleButton', { static: false }) toggleButton!: ElementRef;
  @ViewChild('icon', { static: false }) icon!: ElementRef;
  @ViewChild('iconCollapse', { static: false }) iconCollapse!: ElementRef;
  @ViewChild('collapseContent', { static: false }) collapseContent!: ElementRef;
  @ViewChild('childContainer', { read: ViewContainerRef }) childContainer!: ViewContainerRef;
  @ViewChild('labelSpan', { static: false }) labelSpan!: ElementRef;

  @Input() element: ElementDto | null = null;
  @Input() parentLayout: string = "";

  isCollapsed = true;
  label: string = "";
  collapsedIcon: string = "";
  expandedIcon: string = "";
  initialRender = true;

  // Icons
  readonly defaultCollapsedIcon: string = "fa-caret-down";
  readonly defaultExpandedIcon: string = "fa-caret-up";

  // Static state cache
  private static stateCache = new Map<string, boolean>();

  constructor(
    private cd: ChangeDetectorRef,
    private attributeService: AttributeHelperService,
    private elementLookupService: ElementLookupService,
    private childBearerService: ChildBearerService
  ) { }

  ngOnInit(): void {
    if (!this.element) return;

    this.elementLookupService.addElementObject(this.element.id, this, this.element);
    this.loadState();
  }

  ngAfterViewInit(): void {
    if (!this.element) return;

    requestAnimationFrame(() => {
      this.setAttributes(this.element!.attributes);
      this.renderChildren();

      setTimeout(() => this.initialRender = false, 50);
    });
  }

  private get cacheKey(): string {
    return `collapse_${this.element?.id || 'unknown'}`;
  }

  private loadState(): void {
    try {
      if (!this.element) return;
      const savedState = localStorage.getItem(`collapse_state_${this.element.id}`);
      if (savedState) {
        const state = JSON.parse(savedState);
        this.isCollapsed = state.isCollapsed;
        CollapseComponent.stateCache.set(this.cacheKey, this.isCollapsed);
        return;
      }

      if (CollapseComponent.stateCache.has(this.cacheKey)) {
        this.isCollapsed = CollapseComponent.stateCache.get(this.cacheKey)!;
      }
    } catch (e) {
      console.error(`Failed to load collapse state: ${e}`);
    }
  }

  private saveState(): void {
    if (!this.element) return;

    try {
      // Update memory cache
      CollapseComponent.stateCache.set(this.cacheKey, this.isCollapsed);

      // Persist to localStorage
      localStorage.setItem(`collapse_state_${this.element.id}`,
        JSON.stringify({ isCollapsed: this.isCollapsed }));
    } catch (e) {
      console.error(`Failed to save collapse state: ${e}`);
    }
  }

  private renderChildren(): void {
    if (!this.element?.children?.length) return;

    this.element.children.forEach(childElement => {
      this.childBearerService.bearChild(
        this.childContainer,
        childElement,
        'flex'
      );
    });
  }

  setAttributes(attributes: AttributeDto[], overWriteCache: boolean = false): void {
    this.label = this.attributeService.findGetAttributeValue("label", attributes, "");
    this.collapsedIcon = this.attributeService.findGetAttributeValue("collapsedIcon", attributes, this.defaultCollapsedIcon);
    this.expandedIcon = this.attributeService.findGetAttributeValue("expandedIcon", attributes, this.defaultExpandedIcon);

    // Only use attribute collapsed state if not already loaded from storage or if overWriteCache is true
    if (overWriteCache || !CollapseComponent.stateCache.has(this.cacheKey)) {
      const initialState = this.attributeService.findGetAttributeValue("collapsed", attributes, "true");
      this.isCollapsed = initialState === "true";
    }

    if (this.toggleButton?.nativeElement) {
      const htmlButton = this.toggleButton.nativeElement;
      htmlButton.className = "d-flex align-items-center cursor-pointer collapsed-header";
      this.attributeService.addClasses(htmlButton, attributes, [], []);
      this.attributeService.addGeneralAttributes(htmlButton, attributes);
    }

    if (this.labelSpan?.nativeElement) {
      const htmlLabelSpan = this.labelSpan.nativeElement;
      htmlLabelSpan.className = "flex-grow-1";

      attributes
        .filter(attr => attr.key === 'class' && typeof attr.value === 'string')
        .map(attr => attr.value)
        .filter(className =>
          className.startsWith('text-') ||
          className.startsWith('fw-') ||
          className.startsWith('fst-') ||
          className.startsWith('fs-')
        )
        .forEach(className => htmlLabelSpan.classList.add(className));
    }

    this.updateIcon(attributes);

    if (overWriteCache) {
      this.saveState();
    }
  }

  toggle(): void {
    this.isCollapsed = !this.isCollapsed;
    this.saveState();
    this.updateIcon(this.element?.attributes || []);
  }

  updateIcon(attributes: AttributeDto[]): void {
    if (!this.iconCollapse?.nativeElement || !this.icon?.nativeElement) return;

    const htmlIconCollapse = this.iconCollapse.nativeElement;
    htmlIconCollapse.className = "icon ms-2 fa";
    htmlIconCollapse.classList.add(this.isCollapsed ? this.collapsedIcon : this.expandedIcon);

    const htmlIconCustom = this.icon.nativeElement;
    htmlIconCustom.className = "icon me-2 fa";

    const iconClass = this.attributeService.findGetAttributeValue("icon", attributes, "");
    if (iconClass) {
      htmlIconCustom.classList.add(iconClass);
    }
  }
}
