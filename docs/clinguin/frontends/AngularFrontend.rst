AngularFrontend
---------------

This frontend was developed using `Angular <https://angular.io/guide/setup-local>`_.
For styling, it uses the `bootstrap <https://getbootstrap.com/>`_ library with `Angular-Boostrap <https://ng-bootstrap.github.io/#/home>`_.
Thus, providing beautiful components out of the box by giving access to Bootstrap classes for styling.
For contributing with new components take a look at the :ref:`Development` section.

.. admonition:: Examples
    

    * `Angular Examples <https://github.com/krr-up/clinguin/tree/master/examples/angular>`_

.. tip::

    It implements most of the elements and attributes of the TkinterFrontend.
    So you can also check the Tkinter Syntax as explaned above and try setting those values.

Atributes
+++++++++

.. note::
    
    Any attribute that is passed that does not fall under this list or the specific attributes of the element,
    will be set as a plain html style in the component


Class 
.....

The class atribute ``class`` will add a  `bootstrap class <https://getbootstrap.com/docs/4.0/utilities/borders/>`_
to any element.
This attribute can apear multiple times.

.. tip::

    **Simplify, use classes!**
    
    It is encouranged to use classes for styling with the predefined colors.
    Must of the attributes found below can be replaced by a bootstrap class.

    Not only that but you can set multiple classes in the same ASP rule using 
    
    ``attr(ID,class,(C1;C2;...))``



Positioning
............

.. _Child layout:

**Child layout**

``child_layout``
    *Description*: With this attribute one can define the layout of the children, i.e. how they are positioned.

    *Values*: For the child-layout four different options exists:
        - ``flex`` (default, tries to do it automatically)
        - ``grid`` (grid-like-specification)
        - ``absstatic`` (if one wants to specify the position with absolute-pixelcoordinates)
        - ``relstatic`` (if one wants to specify the position with relative-pixel coordinates(from 0 to 100 percent, where 0 means left/top and 100 means right/bottom)).
        
        They can either bespecified via a clingo symbol or via a string (string is case-insensitive).


.. _Grid:

**Grid**

``grid_column``
    *Description*: With this attribute one can define in which column the element shall be positioned.
    
    *Values*: Integer

``grid_row``
    *Description*: With this attribute one can define in which row the element shall be positioned.
    
    *Values*: Integer

``grid_column_span``
    *Description*: With this attribute one can define, that the elements stretches over several columns.
    
    *Values*: Integer

``grid_row_span``
    *Description*: With this attribute one can define, that the elements stretches over several rows.
    
    *Values*: Integer
    


.. _Relative and Absolute:

**Relative and Absolute**

``pos_x``
    *Description*: With this attribute one sets the x-position of the element - it depends on the parents ``child-layout`` how this is defined (either pixels, relative as a percentage, ...).

    *Values*: Integer

``pos_y``
    *Description*: With this attribute one sets the y-position of the element - it depends on the parents ``child-layout`` how this is defined (either pixels, relative as a percentage, ...).

    *Values*: Integer


.. _Direction:

**Direction**

.. tip ::

    Try using `boostrap positioning <https://getbootstrap.com/docs/4.0/utilities/flex/>`_  instead.


``flex_direction``
    *Description*: With this attribute one can set the ``direction`` (i.e., where it gets placed) of anelement which root has a specified flex layout.

    *Values*: For the flex-direction type two possible values exist:
        - ``column`` (vertical alignment)
        - ``row`` (horizontal alignment).

Style
.....

.. _Color:

**Color**

.. tip ::

    Try using `boostrap colors <https://getbootstrap.com/docs/4.0/utilities/colors/>`_  instead.


``background_color``
    *Description*: With this attribute one can define the background-color of the element.

    *Values*: Color

``foreground_color``
    *Description*: With this attribute one can set the foreground-color of the element.

    *Values*: Color

``border_color``
    *Description*: With this attribute one may set the border color.

    *Values*: Color

``on_hover``
    *Description*: With this attribute one can enable or disable on-hover features for the element.

    *Values*: For the boolean type, either true or false are allowed - either as string or as a clingo-symbol. If one provides it as a string, it is case-insensitive.

``on_hover_background_color``
    *Description*: With this attribute one can set the background color the element shall have, when on_hover is enabled.

    *Values*: Color

``on_hover_foreground_color``
    *Description*: With this attribute one can set the forground color the element shall have, when on_hover is eneabled.

    *Values*: Color

``on_hover_border_color``
    *Description*: With this attribute one can set the color the border of the element shall have, when on_hover is enabled.

    *Values*: Color


.. _Size:

**Size**

``height``
    *Description*: With this attribute one can set the height in pixels of the element.

    *Values*: Integer

``width``
    *Description*: With this attribute one can set the width in pixels of the element.

    *Values*: Integer


.. _Border:

**Border**

.. tip ::

    Try using `boostrap borders <https://getbootstrap.com/docs/4.0/utilities/borders/>`_ instead.

``border_width``
    *Description*: With this attribute one defines the width of the border in pixels.

    *Values*: Integer

``border_color``
    *Description*: With this attribute one may set the border color.

    *Values*: Color

.. _Visibility:                

**Visibility**

``visibility``
    *Description*: Sets the visibility of an element. It can be used to show things like a modal or a container using the update functionality

    *Values*: The visibility, options are:
        -  ``visible``: To show the element
        -  ``hidden``: To hide the element

.. _Text:

**Text**

.. tip ::

    Try using `boostrap text <https://getbootstrap.com/docs/4.0/utilities/text/>`_ style instead.


Elements
++++++++


``window``
..........

The main window of the UI. It is necesary to especify exacly one element of this type.

``menu-bar``
............

The menu bar that apear on top.
Notice that any button which is a children of this element will be placed as part of the menu.

**Attributes**

``icon``
    *Description*: The main icon of the application

    *Values*: `Font awesome <https://fontawesome.com/search?o=r&m=free>`_ symbol name

``title``
    *Description*: The title shown in the uper lext corner

    *Values*: String


``message``
............

A message shown to the user in the bottom.  Corresponds to a `boostrap alert <https://getbootstrap.com/docs/4.0/components/alerts/>`_.
It must always be contained in the window element.

This element is also used internally to send messages from the server to the UI.

**Attributes**

:ref:`Visibility <Visibility>`


``type``
    *Description*: With this attribute one can set the look

    *Values*: For the popup-types three different options exists: 'info' (Default information message),'warning' and 'error'

``title``
    *Description*: With this attribute one can set the title of the alert.

    *Values*: String, can either be specified as a string or if it is simple as a symbol.

``message``
    *Description*: With this attribute one can set the message of the alert.

    *Values*: String, can either be specified as a string or if it is simple as a symbol.


``context-menu``
................


A context menu that will open in the position of the click.
It must always be contained in the window element.
All buttons inside this element will apear as options.


**Attributes**
    
    :ref:`Visibility <Visibility>`

``modal``
.........


A modal pop-up window.
Implemented using `boostrap modals <https://getbootstrap.com/docs/4.0/components/modal/>`_.
It must always be contained in the window element.

**Attributes**
    
:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`

``title``
    *Description*: The title of the modal

    *Values*: String

``container``
.............

A container for defining layout.
Implemented using `boostrap modals <https://getbootstrap.com/docs/4.0/components/modal/>`_.

**Attributes**
    
:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Child layout <Child layout>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`

``title``
    *Description*: The title of the modal

    *Values*: String

``button``
..........

A button.
Implemented using `boostrap buttons <https://getbootstrap.com/docs/4.0/components/buttons/>`_.

**Attributes**
    
:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`

``label``
    *Description*: The text inside the button

    *Values*: String

    ``icon``
    *Description*: The icon of the button

    *Values*: `Font awesome <https://fontawesome.com/search?o=r&m=free>`_ symbol name

``label``
.........

A label.

**Attributes**
    
:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`

``label``
    *Description*: The text inside the button

    *Values*: String


``textfield``
.............

A text field. The value of the text field can be stored on the context using the event ``input``.
See the :ref:`Context` section for more details.
    
**Attributes**
    
:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`

``placeholder``
    *Description*: The text inside the textfield before it is filled

    *Values*: String


``dropdown-menu``
.................

A dropdown menu for single select.
    
**Attributes**
    
:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`

``selected``
    *Description*: The value apearing as selected

    *Values*: String

``dropdown-menu-item``
......................

An item inside a dropdown menu. Must be contained in a dropdown menu.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`

``label``
    *Description*: The text inside the item

    *Values*: String

``canvas``
...........

A canvas to render images.

Canvas can be used to render clingraph images, see :ref:`ClingraphBackend` for details.

**Attributes**
    
:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`

``image``
    *Description*: The local path to the image

    *Values*: String