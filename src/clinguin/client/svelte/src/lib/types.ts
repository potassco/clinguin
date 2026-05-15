
/**
 * attr/3
 * Example: attr(my_button, label, "Click me").
 */
type ClinguinAttribute = {
    id: string;
    key: string;
    value: string | number | boolean;
};

/**
 * when/4
 * Example: when(my_button, click, call, next_solution).
 *
 * action (e.g. "call", "update", "context")
 * operation: the operation string passed to the backend for "call" actions
 */
type ClinguinWhen = {
    id: string;
    event: string;
    action: string;
    operation?: string;
};

/**
 * elem/3
 * Example: elem(my_button, button, my_window).
 */
type ClinguinNode = {
    id: string;
    type: string;
    parent: string;
    attributes?: ClinguinAttribute[];
    when?: ClinguinWhen[];
    children?: ClinguinNode[];
};

/** Shape of the JSON response from GET /info. */
type InfoResponse = {
    status: string;
    version: number;
    active_sessions: number;
    ui?: ClinguinNode;
    ds?: unknown;
};

export type { ClinguinAttribute, ClinguinWhen, ClinguinNode, InfoResponse };
