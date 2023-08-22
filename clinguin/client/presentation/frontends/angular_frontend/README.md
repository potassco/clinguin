## Clinguin Angular Frontend Readme 

Contained in this folder is what can be considered a first draft for a web based frontend option realized in clinguin. 
It is currently highly specific to svgs returned by clingraph, but as described in the section "outlook" there are several ideas 
on how to improve on this. 

### Basic setup
The frontend currently connects to a server located at localhost:8000 and expects a svg image as  well as 
a custom options data structure, which is provided by the ClingraphInteractiveBackend.
On startup an initial request is made, and the "basic" graph is requested.
The response is said "basic" graph, as well as the aforementioned options data structure. 
This data structure is a list of what is currently called "NodeOptions" (misleading, as they can also represent options for components which are not nodes) representing the available options for a specific graph/svg component with a specific ID.
Or in other words, for every ID (of, for example, a node, or an edge) a list of options is saved. 
These NodeOptions follow the following structure: 

 ```typescript
export interface NodeOptions {
    id: string,
    compType: string
    options: (Input_Option|Select_Option)[]
}
 ```
Input_Option and Select_Option represent an Input element and a Select element respectively. 
These are structured as follows: 

```typescript
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
```

### Click handling

A list of such NodeOptions is sent to the Frontend, together with the associated graph. 
On the webpage, the svg content is handed to a div element as an inner HTML. 
The div element listens for "click" events, and then checks if the click has been on a node, or on an edge. 
This classification is made according to the structure of svgs returned by Clingraph, where "g" elements are wrapped around 
the contents of nodes and edges. Upon checking whether the element clicked has a "g" element as it's parent, the ID of the node is extracted from the "title"
element and the ID attribute of the "g" element is checked to see whether the clicked element is a node or an edge.
In Clingraph, the IDs of "g" elements for nodes start with "node" followed by a number, whereas the ones for edges start with "edge".

### Display of Options

Once the ID is extracted, we query our list of NodeOptions, and extract the List of Options for that particular ID. 
Through Angular, the contents of that list are now represented as input fields depending on the type of the Input_Options or as 
Select fields if the option is a Select_Option.
Using Angular functionality we create a FormGroup in order to have an easy two-way binding between the contents of our form and the values of the 
options in question. 
Should a user switch between nodes/edges by clicking on a different one, the contents of the current fields are saved into the NodeOptions 
data structure (see the "state" attribute of the Input_Options and Select_Options data type).
This ensures that changes made to the options of one component are not lost. 

### Submitting the options
Should a user now click the "submit" button, the contents of the form are again saved into the data structure and the data structure 
is currently transformed into ASP-facts of type user_input/5.
user_input looks like this: 

```
user_input(COMPONENT_TYPE,ID,TYPE,NAME,VALUE)
```

COMPONENT_TYPE in this case refers to whether the component in question is a node, edge etc. whereas TYPE
refers to the kind of input type. ID, NAME and VALUE are self explanatory. 
The data structure is thus transformed into a set of ASP facts which are then sent to the Backend, which in turn uses these facts
to alter the answer sets which have created the initial clingraph graph. The result is a changed graph, representing the changes
made through the options by the user (assuming that the logical programs given to the backend were sound).
This graph, as well as the new altered list of options are then again send to the Frontend, where the process is repeated. 


### Outlook 

This example is obviously highly specific to Clingraph, but several possible ways have been proposed to generalize the approach. 
Currently, the setup used makes use of the ClinguinBackend class for the backend implementation, but 
does not use an ui.lp, meaning that no actual clinguin syntax is being used. The angular frontend is thus hard coded and cannot be used with a different backend, 
or deal with clinguin user input. 

The long term goal would be that interactive web based frontends could be possible for any clinguin program, but as a 
first step, an attempt should be made to generalize the current setup, so that the json hierarchy used to 
visualize a clinguin frontend in tkinter can also be used to visualize it in Angular with the ability to 
customize svg interactivity through it. 

Displaying the json hierarchy, a traditional clinguin backend sends based on a ui.lp, is not a trivial task, but can be done 
by writing a parser or something similar. 
For now, we want to focus on how to represent svg interactivity in clinguin syntax. 
An idea that we have come up with, is to add another predicate to the pool of existing ones in clinguin.
Currently, clinguin uses three main predicates. These are, from the documentation:

```
element(ID,TYPE,PARENT): Corresponds to an element in the Gui (button, frame, etc).

attribute(ID_OF_ELEMENT,KEY,VALUE): Used to set various attributes of an element, (background-color, font, etc).

callback(ID_OF_ELEMENT,ACTION,POLICY): Used to define how an element behaves (how = policy) on certain actions.
```

Several challenges have to be addressed. Clingraph cannot be assumed to always be the source of SVG imagery, 
so depending on the SVG, the particular component which constitutes a node or what the user actually wishes to be able 
to interact with could be quite different from clingraph. It should therefore be possible to specify a target component, 
as some knowledge in regard to the svg that is to be interacted with can be assumed. 

Second, the issue of locating an identifier in the SVG needs to be addressed. It can be assumed that there is some connection between 
an identification of a term in an Answer Set Program and an identification in an SVG. 
Different components of the same type are separated by their identification and this identification should also be found somewhere 
in the SVG. 
As Clingraph itself shows, however, the ID is not necessarily always at the first spot one would assume it to be in
(such as e.g. in the "id" attribute of the HTML element), where the ID of the node/1 predicate was found in the "title" SVG element. 
We therefore need a functionality that allows a user to specify, where such an identification can be found. 
This identification should be corresponding to an ID set in the list of NodeOptions, so that options can be loaded 
for the respective component. 

Thirdly, though more related to future endeavors, a user should be able to decide what exactly happens, 
when he clicks upon a specific area of the SVG. For now, we will leave it as a given, that 
the interaction will be limited to the loading of options. 

In order to seperate interactivity from the rest, we propose the addition of a forth predicate in order to solve the first two issues:

```
interact(SVG_ID, ELEMENT_NAME, SCOPE, ID_LOCATION)
```

SVG_ID would refer to the ID of the SVG in question (specified at an earlier point with an element 
predicate), ELEMENT_NAME refers to the name of the HTML Element which should be selected. 
SCOPE refers to the location of the element relative to the place clicked.
To illustrate, an example from clingraph. 
An example node in an svg produced by clingraph is modelled as follows:

```html
<g id="node2" class="node">
    <title>3</title>
    <ellipse fill="green" stroke="green" cx="99" cy="-162" rx="27" ry="18"/>
    <text text-anchor="middle" x="99" y="-158.3" font-family="Times New Roman,serif" font-size="14.00">3</text>
</g>
```

If we executed something when the "g" element is clicked, the code would not execute, as the click would
fall on the ellipse, or the text, or the title. However, the "g" element still represents the node in its entirety, as it contains 
everything in relation to one node (or in the case of clingraph, an edge). 
In this case we would want to execute something, in case the PARENT of the element which is clicked 
is a "g" element. SCOPE should therefore represent this, whether the element specified in ELEMENT_NAME, which we want to extract, is a 
PARENT, an ANCESTOR, a CHILD of the element clicked, or the element itself. 
To illustrate: in the example node above, ELEMENT_NAME would be "g" and SCOPE would be "PARENT", as the click event falls 
on one of the elements within the "g" element, but we want to extract the "g" element itself.

The ID_LOCATION allows a user to specify, where the identification of the component which was clicked can be 
found, relative to the element extracted in ELEMENT_NAME. 
An example notation for this, which could be used, would be described thusly: 

```
LOCATION ->  SCOPE | ATTRIBUTE:NAME | content 
SCOPE -> SCOPE_NAME:ELEMENT_NAME:LOCATION 
SCOPE_NAME -> child | parent 
ELEMENT_NAME -> STRING
NAME -> STRING 
ATTRIBUTE -> STRING
```

The user could therefore describe the location in a way quite similar to how parents or children are accessed in JavaScript. 

The information thus contained within the input element could be sent to the backend, which then sends the data to the frontend. 
The frontend could then extract specific identifications from specific parts of the SVG, representing components which 
can be enriched with options for dynamic changes. 
This would be but a first step towards full SVG interactivity, but it would theoretically allow user specified 
interactivity for any SVG, provided that the user has knowledge of the SVGs structure. 

