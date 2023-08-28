import { AfterViewInit, ChangeDetectorRef, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, FormControl } from '@angular/forms';
import { GraphRequest, ClingraphVizDto } from '../types/messageTypes';
import { NodeOptions, Input_Option, Select_Option } from '../types/options';
import { ASPtranslateService } from '../asptranslate.service';
import { ElementDto } from 'src/app/types/json-response.dto';
import { AttributeHelperService } from 'src/app/attribute-helper.service';
import { DrawFrontendService } from 'src/app/draw-frontend.service';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements AfterViewInit {
  @Input() element: ElementDto | null = null

  @ViewChild("svgContainer")
  svgContainer!:ElementRef;

  optionsForm: FormGroup = new FormGroup({})
  svgString = ""
  type = ""
  nodeOptionsList:NodeOptions[] = []
  currID: string = ""
  optionsList: (Input_Option|Select_Option)[] = []
  errStr: string = ""

  constructor(private attributeService: AttributeHelperService, private frontendService: DrawFrontendService, private fb:FormBuilder, private cd: ChangeDetectorRef, private aspService:ASPtranslateService){}
    //private svgService: SvgServiceService  }
  ngAfterViewInit(): void {

    if (this.element != null) {

      let data = this.attributeService.findAttribute("clingraph_interactive", this.element.attributes)
      if (data != null) {
        let clingraph_viz_data : ClingraphVizDto = data as ClingraphVizDto

        this.svgString = clingraph_viz_data.data;
        this.svgContainer.nativeElement.innerHTML = this.svgString

        this.nodeOptionsList = clingraph_viz_data.option_data; 
        console.log("NodeOptions after init:", this.nodeOptionsList)
        console.log("form after init: ",this.optionsForm)

        this.cd.detectChanges()
      }

    }
  }

  retrieveSelectOptions(opt:(Input_Option|Select_Option)){
    if("options" in opt){
      return opt.options
    } else {
      return []
    }
  }

  handleNodeClick(event:Event){
    console.log("clicked")
    let element = event.target as HTMLElement
    let parent = element.parentNode as HTMLElement
    console.log(element)
    console.log(parent)
    if(parent !== null && parent.nodeName == 'g'){
      console.log("past first")
      let title = parent.getElementsByTagName("title")[0]
      console.log(title)
      if(title !== null){
        console.log("past second")
        const compId = title.textContent
        if(compId !== null && compId !== ""){
          if(parent.id.startsWith("node")){
            console.log("clicked node with ID: ", compId)
            this.type = "node"
            this.updateOptions(compId, "node")
          } else if(element.id.startsWith("edge")){
            console.log("clicked")
            this.type = "edge"
            this.updateOptions(compId, "edge")
          }
        }
      }
    }
  }

  checkClick(event:Event){
    console.log("clicked box")
    let target = (event.target as HTMLElement)
    console.log(target.getAttribute("value"))
    console.log(target.getAttribute("checked"))
    console.log("form: ",this.optionsForm)
  }

  updateOptions(id:string, compType:string){
    this.optionsList.forEach((val) => {
      val.state = this.optionsForm.value[val.name]
    })
    this.currID = id
    let list = this.nodeOptionsList.filter((val) => {return val.id == id && val.compType == compType})
    if(list.length != 1){
      console.log(`Something went wrong: There is more than one or no node/edge with id ${id} in the options list!`)
      this.errStr = `Something went wrong: There is more than one or no node/edge with id ${id} in the options list!`
    } else {
      this.optionsList = list.map(((val) => {return val.options})).flat()
      let group = new FormGroup({})
      this.optionsList.forEach((val) => {
        if(val.type == "checkbox"){
          let check = val.state == "true" || val.state == true ? true : false
          group.addControl(val.name,new FormControl(check))
        } else {
          group.addControl(val.name,new FormControl(val.state))
        }
      })

    this.optionsForm = group
    console.log("form after update: ",this.optionsForm)
    console.log(this.nodeOptionsList)
  }
}

  submitForm(){
    this.errStr = ""
    let asp: string[] = []
    let form = this.optionsForm.value
    console.log("Form: ", form)
    this.optionsList.forEach((val) => {
        val.state = form[val.name]
      })
    this.nodeOptionsList.forEach((val) => {val.options.forEach((opt) => {
      asp.push(this.aspService.toUserInputASP(val.compType,val.id,opt.type,opt.name,opt.state))
    })})
    let aspString:string = asp.join(",")
    let req = {"function":`graphUpdate(${aspString})`}
    console.log(req)

    this.frontendService.uncheckedPost(req as GraphRequest)
  }
  
}
