import { NodeOptions } from "./options"

export interface GraphRequest {
    function: string
}

export interface GraphResponse {
    data: string,
    option_data: NodeOptions[]
}
