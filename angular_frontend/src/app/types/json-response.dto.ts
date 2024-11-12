

export interface JsonResponse {
    root: ElementDto
}

export interface ElementDto {
    id: string,
    type: string,
    parent: string,
    attributes: AttributeDto[],
    when: WhenDto[],
    children: ElementDto[]
}

export interface AttributeDto {
    id: string,
    key: string,
    value: string
}


export interface WhenDto {
    id: string,
    actionType: string,
    interactionType: string,
    operation: string,
    event?: string,
    action?: string
}
