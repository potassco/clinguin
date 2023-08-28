import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Input_Option, Select_Option } from '../types/options';

@Component({
  selector: 'app-graph-options',
  templateUrl: './graph-options.component.html',
  styleUrls: ['./graph-options.component.scss']
})
export class GraphOptionsComponent {
  @Input() optionsList!:(Input_Option|Select_Option)[]
  @Input() optionsForm!:FormGroup
  @Input() compID:string = ""
  @Output() submitEvent = new EventEmitter<string>()

  constructor(){}

  retrieveSelectOptions(opt:(Input_Option|Select_Option)){
    if("options" in opt){
      return opt.options
    } else {
      return []
    }
  }

  submitForm(){
    this.submitEvent.emit("");
  }


}
