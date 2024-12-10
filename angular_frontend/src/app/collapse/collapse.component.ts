import { ChangeDetectorRef, Component, ElementRef, Input, ViewChild, ViewContainerRef } from '@angular/core';
import { AttributeDto, ElementDto } from '../types/json-response.dto';
import { AttributeHelperService } from '../attribute-helper.service';
import { ElementLookupService } from '../element-lookup.service';
import { NgbCollapse } from '@ng-bootstrap/ng-bootstrap';
import { ChildBearerService } from '../child-bearer.service';

@Component({
  selector: 'app-collapse',
  templateUrl: './collapse.component.html'
})
export class CollapseComponent {
  @ViewChild('toggleButton', { static: false }) toggleButton!: ElementRef;
  @ViewChild('icon', { static: false }) icon!: ElementRef;
  @ViewChild('collapseContent', { static: false }) collapseContent!: ElementRef;
  @ViewChild('childContainer', { read: ViewContainerRef }) childContainer!: ViewContainerRef;
  @ViewChild(NgbCollapse) ngbCollapse!: NgbCollapse;

  @Input() element: ElementDto | null = null;
  @Input() parentLayout: string = "";

  isCollapsed = true; // Tracks whether the content is collapsed or expanded
  label: string = ""; // Label for the collapse button

  // Default icons
  defaultCollapsedIcon: string = "fa fa-caret-right"; // Default collapsed icon class
  defaultExpandedIcon: string = "fa fa-caret-down"; // Default expanded icon class

  constructor(
    private cd: ChangeDetectorRef,
    private attributeService: AttributeHelperService,
    private elementLookupService: ElementLookupService,
    private childBearerService: ChildBearerService
  ) {}

  ngAfterViewInit(): void {
    if (this.element != null) {
      this.elementLookupService.addElementObject(this.element.id, this, this.element);

      this.setAttributes(this.element.attributes);

      setTimeout(() => {
        if (this.element?.children && this.element.children.length > 0) {
          this.element.children.forEach(childElement => {
            this.childBearerService.bearChild(
              this.childContainer,
              childElement,
              'flex'
            );
          });
        }
        this.cd.detectChanges();
      });
    }
  }

  setAttributes(attributes: AttributeDto[]) {
    // Set label and initial collapsed state
    this.label = this.attributeService.findGetAttributeValue("label", attributes, "");
    const initialState = this.attributeService.findGetAttributeValue("collapsed", attributes, "true");
    this.isCollapsed = initialState === "true";

    let htmlButton = this.toggleButton.nativeElement;
    let htmlIcon = this.icon.nativeElement;

    this.attributeService.addAttributes(htmlButton, attributes);
    this.attributeService.addClasses(htmlButton, attributes, [], []);
    this.attributeService.addGeneralAttributes(htmlButton, attributes);

    this.updateIcon(attributes);

    this.cd.detectChanges();
  }

  // Toggle collapse state and update the icon dynamically
  toggle() {
    this.isCollapsed = !this.isCollapsed; // Switch between collapsed and expanded states

    // Update icon classes based on the current state
    if (this.icon && this.element?.attributes) {
      this.updateIcon(this.element.attributes);
    }

    this.cd.detectChanges(); // Trigger change detection after toggling
  }

  // Update icon based on collapse state
  updateIcon(attributes: AttributeDto[]) {
	const htmlIcon = this.icon.nativeElement;
	htmlIcon.className = "icon";
  
	// Check for collapsed/expanded specific icons
	const iconAttrName = this.isCollapsed ? "collapsed_icon" : "expanded_icon";
  
	// Check for the icon for both states
	const specificIcon = this.attributeService.findGetAttributeValue(iconAttrName, attributes, "");
	const generalIcon = this.attributeService.findGetAttributeValue("icon", attributes, "");
  
	// Determine which icon to use
	let iconClass = specificIcon || generalIcon;
  
	// Handle 'none' case to hide the icon
	if (iconClass.toLowerCase() === "none") {
	  htmlIcon.style.display = "none"; // Hide the icon element
	} else {
	  htmlIcon.style.display = ""; // Ensure the icon is visible
	  if (iconClass) {
		htmlIcon.classList.add(...iconClass.split(" "));
	  } else {
		const defaultIcon = this.isCollapsed ? this.defaultCollapsedIcon : this.defaultExpandedIcon;
		htmlIcon.classList.add(...defaultIcon.split(" "));
	  }

	  htmlIcon.style.paddingRight = "8px";
	}
  }
}