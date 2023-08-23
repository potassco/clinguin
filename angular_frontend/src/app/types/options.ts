export interface Input_Option {
    name: string,
    type: string,
    state: any
}

export interface Select_Option {
    name: string
    type: string
    state: any
    options: string[]
}

export interface NodeOptions {
    id: string,
    compType: string
    options: (Input_Option|Select_Option)[]
}