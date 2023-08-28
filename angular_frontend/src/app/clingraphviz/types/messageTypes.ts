import { AttributeDto } from "src/app/types/json-response.dto"
import { NodeOptions } from "./options"

export interface GraphRequest {
    function: string
}

export interface ClingraphVizDto extends AttributeDto {
    data: string,
    option_data: NodeOptions[]
}