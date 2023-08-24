
export interface JsonResponse {
    root: ElementDto
}

export interface ElementDto {
    id: string,
    type: string,
    parent: string,
    attributes: AttributeDto[],
    callbacks: CallbackDto[],
    children: ElementDto[]
}

export interface AttributeDto {
    id: string,
    key: string,
    value: string
}

export interface CallbackDto {
    id: string,
    action: string,
    policy: string
}
