import { ChangeDetectorRef, Component, ComponentRef, ElementRef, ViewChild, ViewContainerRef } from '@angular/core';
import { AttributeDto, ElementDto, WhenDto } from 'src/app/types/json-response.dto';
import { AttributeHelperService } from 'src/app/attribute-helper.service';
import { DrawFrontendService } from '../draw-frontend.service';
import { ElementLookupService } from '../element-lookup.service';
import { ComponentCreationService } from '../component-creation.service';
import { ChildBearerService } from '../child-bearer.service';
import { ContextMenuService } from '../context-menu.service';
import { CallBackHelperService } from '../callback-helper.service';

@Component({
  selector: 'app-new-main',
  templateUrl: './window.component.html',
  styleUrls: ['./window.component.scss']
})
export class WindowComponent {
  @ViewChild('parent',{static:false}) parent!: ElementRef;
  @ViewChild('child',{read: ViewContainerRef}) child!: ViewContainerRef;

  element : ElementDto | null = null

  children: ComponentRef<any>[] = []

  window_id: string = ""
  window: ElementDto | null = null

  menuBar: ElementDto | null = null
  messageList: ElementDto[] = []
  contextMenuList: ElementDto[] = []
  
  constructor(private childBearerService: ChildBearerService, private attributeService: AttributeHelperService, private cd: ChangeDetectorRef, private frontendService: DrawFrontendService, private elementLookupService: ElementLookupService, private contextMenuService: ContextMenuService, private callbackService: CallBackHelperService) {
  }

  ngAfterViewInit(): void {

    this.frontendService.messageLists.subscribe({next: data => {
      this.messageList = data
      this.cd.detectChanges()
    }})

    this.frontendService.frontendJson.subscribe({next: (data:ElementDto) => {

      console.log(data)

      this.children.forEach(child => {
        this.child.clear()
      })
      this.children = []

      this.cleanValues(data)

      this.frontendService.detectCreateMenuBar(data)

      let messageList : ElementDto[] = []
      let contextMenus : ElementDto[] = []
      this.frontendService.getAllMessagesContextMenus(data, messageList, contextMenus)
      this.frontendService.messageLists.next(messageList)

      this.frontendService.contextMenus.subscribe(data => {
          data.forEach((item:ElementDto) => {
              this.contextMenuService.registerContextMenu(item.id, item)
          })
          this.contextMenuList = data
      })

      this.frontendService.contextMenus.next(contextMenus)

      let window = data.children[0]

      this.window_id = window.id


      this.element = window
      this.window = window

      this.cd.detectChanges()

      let childLayout = this.attributeService.findGetAttributeValue("child_layout",window.attributes,"flex")

      this.elementLookupService.addElementAll(this.window_id, this, this.parent.nativeElement, window)

      window.children.forEach(item => {
        let my_comp = this.childBearerService.bearChild(this.child, item, childLayout)
        if (my_comp != null) {
          this.children.push(my_comp)
        }
      })

      this.setAttributes(window.attributes)
      this.doCallbacks(window.when)
      // Prevents Errors
      this.cd.detectChanges()
    },
    error: (err) => console.log(err)})

    this.frontendService.initialGet()
  }

  setAttributes(attributes: AttributeDto[]) {
      let parentHTML = this.parent.nativeElement
      this.attributeService.setChildLayout(parentHTML, attributes)
      this.attributeService.addAttributes(parentHTML, attributes)
      this.attributeService.addClasses(parentHTML, attributes,[],[])
      
      this.cd.detectChanges()
  }

  doCallbacks(whens:WhenDto[]) {
    let parentHTML = this.parent.nativeElement
    this.callbackService.setCallbacks(parentHTML, whens)
  }
  
  cleanValues(element: ElementDto) {
    for (let i = 0; i < element.attributes.length; i++) {
      let value = element.attributes[i].value
      value = this.stringSanitizer(value)
      element.attributes[i].value = value

      let key = element.attributes[i].key
      key = this.stringSanitizer(key)
      element.attributes[i].key = key

      if (key != "image") {
        value = value.replace("\\n","<br>")
      }
    }

    for (let i = 0; i < element.when.length; i++) {
      if (element.when[i].action_type !== undefined) {
        element.when[i].actionType = element.when[i].action_type!
      }
      if (element.when[i].interaction_type !== undefined) {
        element.when[i].interactionType = element.when[i].interaction_type!
      }

      let policy = element.when[i].policy
      policy = this.stringSanitizer(policy)
      element.when[i].policy = policy

      let action = element.when[i].actionType
      action = this.stringSanitizer(action)
      element.when[i].actionType = action

      let interaction = element.when[i].interactionType
      interaction = this.stringSanitizer(interaction)
      element.when[i].interactionType = interaction
    }

    element.children.forEach(child => {
      this.cleanValues(child)
    })
  }

  stringSanitizer(value:string) : string {
    if (value == null) {
      return value
    }
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

    return value
  }


}
