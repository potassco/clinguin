Angular Frontend Development
============================

This section is for development and contribution in the AngularFrontend.
For instance to create new element types. Unlike the custom backends, this changes must be done inside the source code of *clinguin*.
Make sure you have installed from source.


.. warning::

    The following is only required for making changes to the web-frontend.

Requirements
------------

    - `NPM <https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>`_
    - `NODE <https://nodejs.org/en/download>`_
    - `Angular <https://angular.io/guide/setup-local>`_

How to run changes
------------------

This process shows changes made on the `angular_fronted` folder in real time.

1. Start the server
    - Replace  ``clinguin client-server`` by ``python start.py server`` on the desired example
2. Start the web client
    - Open a new tab
    - Navigate to the folder `/angular_frontend`.
    - Type ``ng serve``
    - Go to the URL `127.0.0.1:4200` in your web-browser.


Compile source code
-------------------

This allows to use the AngularFrontend by passing the ``--frontend`` argument to the client.

Be sure that you have `make` and all the dev-tools for the web-frontend installed (`Angular`), as detailed below! Then type:

.. code-block:: console

    $ make angular

This builds the frontend, and then installs `clinguin`.



Internal Workflow
-----------------

The web-frontend is a kind of non-typical `Angular <https://angular.io/guide/setup-local>`_ frontend. The reason for this lies in the nature of clinguin, as the frontend has to be built dynamically, with all its challenges.

The JSON that is passed to the frontend contains all the information needed for the frontend to create a corresponding GUI. Due to the hierarchical tree-like nature of the JSON, the frontend is created in a tree-traversal manner, starting with the *window*.

**Elements/Components**

Most *element* (s), such as *window*, correspond to a **component** in the web-frontend (`component <https://angular.io/api/core/Component>`_; `How to create a component? <https://angular.io/tutorial/tour-of-heroes/toh-pt3>`_). Note that e.g. the *dropdown_menu_item* element is not a unique component but part of the *dropdown_menu* component.

Regarding the structure of such an **element-component**, the *element*-variable, which is of the *ElementDto* type, resembles the *element* predicate of the logic-program and has importantly the *children*, *attributes*, and *do* lists, and the *id* and *type* variables. These variables and lists are used to set the look, feel, and behavior of the components. The *attributes* are generally set in the *setAttributes* method, which is called to change the look of a component (so not only initially but importantly also on an update in the frontend).

The *when* is set one time in the initial construction of the component (in the `ngAfterViewInit-Lifecycle <https://angular.io/guide/lifecycle-hooks>`_), by getting the *nativeHtml* element. This *nativeHtml* corresponds to the *dom*-element (`dom-element <https://www.w3schools.com/jsref/dom_obj_all.asp>`_), where one can DIRECTLY set the style or set the content of an `HTML-Tag <https://www.w3schools.com/tags/tag_html.asp>`_ directly as a string. As we do not know which components exist in which configuration prior to receiving a backend response, we need to dynamically create them. We use the **componentCreationService** (see below) for this task.

Note that the components *menu-bar*, *context-menu*, and *message* deviate a bit from this general tree-traversal. Only one *menu-bar* can exist, and it is placed at the *top-level*, therefore it is statically placed in the *app.component.html*. The *context-menu* and *message* components deviate from the rest, as they need to be placed at specific positions, relative to the *viewport*. Therefore, they are placed into the *window.component.html*.

**Services**

The `Angular-services <https://angular.io/guide/architecture-services>`_ are described next, which add all the *fancy* functionalities, like calling the backend, etc.

Important services and their description:

* **HttpService**: Service that configures how get/post-requests are sent to the backend. Note that the actual event is NOT handled here but just a *subscribable/observable* is returned.
* **DrawFrontendService**: One of the most important services. It acts as a data-store for the JSON and also for other important data (like the menu-bar, context-menus, and alerts/messages). The data-store is implemented in an `RXJS <https://www.learnrxjs.io/>`_ fashion, which implements the asynchronous `subscriber-publisher <https://rxjs.dev/guide/subscription>`_ principle. This service subscribes to the return values of the **HttpService**, therefore this service handles how the response from the backend is treated.
* **ElementLookupService**: An important service for setting the look, feel, and behavior of the components. It acts as a data-store (non-RXJS type), which stores objects of components/elements.
* **ComponentCreationService**: Service that dynamically creates components. If one wants to add **new components, this needs to be specified here!**.
* **ChildBearerService**: Closely related to the *ComponentCreationService* is this service, which handles the call of the correct attribute-handling-methods, to ensure correct placement, etc. Note that the *ChildBearerService* calls the *ComponentCreationService*. The name derives from the fact that it adds looks to the newly created component. With the values of this data-store, one is able to set dynamically the shared element methods (like *setAttributes*).
* **ContextService**: Data-store (non-RXJS type) for the context, i.e., the key-value pair that resides both in the frontend and in the backend.
* **ModalRefService**: Data-store (non-RXJS type) for the modals. Needed for ensuring that modals are reloaded/closed when getting backend responses.
* **ContextMenuService**: Data-store (non-RXJS type) for the context-menus. Needed to ensure the context-menus are closed/opened properly (indirectly) Implements useful methods that are needed for the context.
* **ConfigService**: Reads the configuration file, where the *server-url* and *server-port* is stored.
* **LocatorService**: Helper service for injecting services into functions.
* **CallbackHelperService**: Handles that the correct event-listener is created for the correct event. Currently handled do-operation-types are *update*, *context*, *call*/*callback*, and *show_context_menu*.
* **AttributeHelperService**: This service ensures a translation between commonly used attributes in clinguin and their corresponding part in *CSS*. Note that it is possible to set **CSS styles directly**, via the *setAttributesDirectly* method. This method is by default always called for all attributes, just note that the attribute-keys have to be in **camelCase** notation (e.g., *align-items* to *alignItems*).
