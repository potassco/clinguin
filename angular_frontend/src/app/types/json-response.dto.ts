import { NodeOptions } from "../clingraphviz/types/options"


export interface JsonResponse {
    root: ElementDto
}

export interface ElementDto {
    id: string,
    type: string,
    parent: string,
    attributes: AttributeDto[],
    do: DoDto[],
    children: ElementDto[]
}

export interface AttributeDto {
    id: string,
    key: string,
    value: string
}


export interface DoDto {
    id: string,
    actionType: string,
    interactionType: string,
    policy: string,
    action_type?: string,
    interaction_type?: string
}
