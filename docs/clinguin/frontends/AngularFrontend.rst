AngularFrontend
---------------

This frontend was developed using `Angular <https://angular.io/guide/setup-local>`_.
For styling, it uses the `bootstrap v5.0 <https://getbootstrap.com/docs/5.0/utilities/flex/>`_ library.
Thus, providing beautiful components out of the box by giving access to Bootstrap classes for styling.
For contributing with new components take a look at the :ref:`Development` section.

.. admonition:: Examples

    * `Angular Examples <https://github.com/krr-up/clinguin/tree/master/examples/angular>`_

.. tip::

    It implements most of the elements and attributes of the TkinterFrontend.
    So you can also check the Tkinter Syntax as explained above and try setting those values.

Elements
++++++++

``window``
..........

The main window of the UI. It is necessary to specify exactly one element of this type.
Behaves as a :ref:`container` element.

.. _container:

``container``
.............

A container for defining layout. See `bootstrap flex <https://getbootstrap.com/docs/5.0/utilities/flex/>`_ for layout ideas.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Child layout <Child layout>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`

``menu-bar``
............

The menu bar that appears on top.
Any button which is a child of this element will be placed as part of the menu.
Only :ref:`button` elements are allowed as part of the menu bar.
Corresponds to a limited version of `bootstrap navbar <https://getbootstrap.com/docs/5.0/components/navbar/>`_.
Menu bar buttons can use the attribute :ref:`Order <Order>`, to set the order of appearance.


**Attributes**

``icon``
    *Description*: The main icon of the application

    *Values*: `Font Awesome <https://fontawesome.com/search?o=r&m=free>`_ symbol name

``title``
    *Description*: The title shown in the upper left corner

    *Values*: String

``message``
............

A message shown to the user at the bottom.
It must always be contained in the window element.
Corresponds to a limited version of `bootstrap alert <https://getbootstrap.com/docs/5.0/components/alerts/>`_.

This element is also used internally to send messages from the server to the UI.

**Attributes**

:ref:`Visibility <Visibility>`

``type``
    *Description*: With this attribute one can set the look

    *Values*: For the popup-types, three different options exist: 'info' (Default information message), 'warning', and 'error'

``title``
    *Description*: With this attribute one can set the title of the alert.

    *Values*: String, can either be specified as a string or as a symbol.

``message``
    *Description*: With this attribute one can set the message of the alert.

    *Values*: String, can either be specified as a string or as a symbol.

``context-menu``
..................

A context menu that will open in the position of the click.
It must always be contained in the window element.
All :ref:`button` elements inside this element will appear as options in a list.

**Attributes**

:ref:`Visibility <Visibility>`

``modal``
.........

A modal pop-up window.
It must always be contained in the window element.
Corresponds to a limited version of `bootstrap modal <https://getbootstrap.com/docs/5.0/components/modal/>`_.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`

``title``
    *Description*: The title of the modal

    *Values*: String

``size``

    *Description*: The size of the modal

    *Values*: String. Can be ``sm`` for small, ``m`` for medium, ``lg`` for large, or ``xl`` for extra large.

.. _button:

``button``
..........

A button.
Corresponds to a limited version of `bootstrap buttons <https://getbootstrap.com/docs/5.0/components/buttons/>`_.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
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

    *Values*: `Font Awesome <https://fontawesome.com/search?o=r&m=free>`_ symbol name

``label``
.........

A label to show text. See `bootstrap text <https://getbootstrap.com/docs/5.0/utilities/text/>`_ for styling.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`

``label``
    *Description*: The text inside the label

    *Values*: String

``textfield``
.............

A text field to input text. The value of the text field can be stored in the context using the event ``input``.
See the :ref:`Context` section for more details.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`

``placeholder``
    *Description*: The text inside the text field before it is filled

    *Values*: String

``dropdown-menu``
.................

A dropdown menu for single select. All children should be :ref:`dropdown-menu-item` elements.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`

``selected``
    *Description*: The value appearing as selected

    *Values*: String

.. tip::

    For multi select, try using a :ref:`checkbox` insted.

.. _dropdown-menu-item:

``dropdown-menu-item``
......................

An item inside a dropdown menu. Must be contained in a dropdown menu.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
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

Canvas can be used to render clingraph images; see :ref:`ClingraphBackend` for details.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`

``image``
    *Description*: The local path to the image

    *Values*: String

``progress-bar``
................

A progress bar component used to display a percentage of completion. Corresponds to a limited version of `Bootstrap progress bars <https://getbootstrap.com/docs/5.0/components/progress/>`_ .


**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`

``value``
    *Description*: The current value of the progress bar. By default, it is set to 0.

    *Values*: Integer

``min``
    *Description*: The minimum value of the progress bar. By default, it is set to 0.

    *Values*: Integer

``max``
    *Description*: The maximum value of the progress bar. By default, it is set to 100.

    *Values*: Integer

``label``
    *Description*: A label displayed inside the progress bar.

    *Values*: String

``out_label``
    *Description*: A label displayed outside the progress bar.

    *Values*: String

.. tip::

    **Percentage**

    If you wish to use percentages, you can pass an interget between 0 and 100 to the value attribute
    and use the default values for min and max; 0 and 100 respectively.


.. _checkbox:

``checkbox``
............

A checkbox component used to display a boolean value. Corresponds to a limited version of `Bootstrap form-check <https://getbootstrap.com/docs/5.0/forms/checks-radios/>`_ .


**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Grid <Grid>`,
:ref:`Relative and Absolute <Relative and Absolute>`,
:ref:`Direction <Direction>`,
:ref:`Color <Color>`,
:ref:`Size <Size>`,
:ref:`Border <Border>`,
:ref:`Text <Text>`


``checked``
    *Description*: The current value of the checkbox. By default, it is set to false.

    *Values*: Boolean. Any value is considered as true. Leaving the attribute undefied defaults to false

``label``
    *Description*: A label displayed next to the checkbox.

    *Values*: String

``disabled``
    *Description*: Disables the checkbox.

    *Values*: Boolean

``type``
    *Description*: The type of the checkbox. By default, it is set to 'checkbox'.

    *Values*: String. Can be 'checkbox' or 'radio'

.. important::

    **Keep checkbox checked**

    When a checkbox is clicked, if an operation is called, the attribute ``checked`` needs to be updated in the encoding to reflect the new value.

    .. admonition:: Example

        .. code-block:: prolog

            elem(check(P), checkbox, included(P)):- person(P).
            attr(check(P), checked, true):- include(P).
            when(check(P), click, call, set_external(include(P),true)) :- person(P), not include(P).
            when(check(P), click, call, set_external(include(P),false)) :- person(P), include(P).

.. tip::

    **Radio buttons**

    If you wish to use a radio button, you can set the type attribute to 'radio'.
    To have a radio-like behavior, you should make sure the condition for the checked attribute is exclusive for each radio button.

    .. admonition:: Example

        The last rule in the following example ensures that only one radio button is checked at a time.

        .. code-block:: prolog

            elem(radio(P), checkbox, included(P)):- person(P).
            attr(radio(P), type, radio):- person(P).
            attr(radio(P), checked, true):- include(P).
            when(radio(P), click, call, set_external(include(P),true)) :- person(P), not include(P).
            when(radio(P), click, call, set_external(include(P'),false)) :- person(P), not include(P), person(P'), P'!=P.


Atributes
+++++++++

.. note::

    Any attribute that does not fall under this list or the specific attributes of the element
    will be set as a plain HTML style in the component.

Class
.....

The class attribute ``class`` will add a `bootstrap class <https://getbootstrap.com/docs/5.0>`_
to most elements.
This attribute can appear multiple times.
It can help to style the element with classes defined for each element type or general Bootstrap classes:

-  `Text classes <https://getbootstrap.com/docs/5.0/utilities/text/>`_
-  `Spacing classes <https://getbootstrap.com/docs/5.0/utilities/spacing/>`_
-  `Color classes <https://getbootstrap.com/docs/5.0/utilities/colors/>`_
-  `Border classes <https://getbootstrap.com/docs/5.0/utilities/borders/>`_
-  `Background classes <https://getbootstrap.com/docs/5.0/utilities/background/>`_
-  `Display classes <https://getbootstrap.com/docs/5.0/utilities/display/>`_
-  `Flexible layout classes <https://getbootstrap.com/docs/5.0/utilities/flex/>`_
-  `Size classes <https://getbootstrap.com/docs/5.0/utilities/sizing/>`_

.. tip::

    **Simplify, use classes!**

    It is encouraged to use classes for styling with the predefined colors.
    Many of the attributes found in this guide can be replaced by a Bootstrap class.

    Not only that but you can set multiple classes in the same attribute using

    ``attr(ID,class,(C1;C2;...))``

Positioning
............

.. _Order:

**Order**

``order``
    *Description*: With this numeric attribute, set the order of appearance for the element inside the parent

    *Values*: Integer

    .. warning::

        Make sure the order is set for all children of the same parent; otherwise, the order will not be respected.

.. _Child layout:

**Child layout**

.. tip::

    Try using `bootstrap flex <https://getbootstrap.com/docs/5.0/utilities/flex/>`_ instead.

``child_layout``
    *Description*: With this attribute, one can define the layout of the children, i.e., how they are positioned.

    *Values*: For the child-layout, four different options exist:
        - ``flex`` (default, tries to do it automatically)
        - ``grid`` (grid-like specification)
        - ``absstatic`` (if one wants to specify the position with absolute-pixel coordinates)
        - ``relstatic`` (if one wants to specify the position with relative-pixel coordinates (from 0 to 100 percent, where 0 means left/top and 100 means right/bottom)).

        They can either be specified via a Clingo symbol or via a string (string is case-insensitive).

.. _Grid:

**Grid**

``grid_column``
    *Description*: With this attribute, one can define in which column the element shall be positioned.

    *Values*: Integer

``grid_row``
    *Description*: With this attribute, one can define in which row the element shall be positioned.

    *Values*: Integer

``grid_column_span``
    *Description*: With this attribute, one can define that the element stretches over several columns.

    *Values*: Integer

``grid_row_span``
    *Description*: With this attribute, one can define that the element stretches over several rows.

    *Values*: Integer

.. _Relative and Absolute:

**Relative and Absolute**

``pos_x``
    *Description*: With this attribute, one sets the x-position of the element - it depends on the parent's ``child-layout`` how this is defined (either pixels, relative as a percentage, etc.).

    *Values*: Integer

``pos_y``
    *Description*: With this attribute, one sets the y-position of the element - it depends on the parent's ``child-layout`` how this is defined (either pixels, relative as a percentage, etc.).

    *Values*: Integer

.. _Direction:

**Direction**

.. tip::

    Try using `bootstrap flex <https://getbootstrap.com/docs/5.0/utilities/flex/>`_ instead.

``flex_direction``
    *Description*: With this attribute, one can set the ``direction`` (i.e., where it gets placed) of an element whose root has a specified flex layout.

    *Values*: For the flex-direction type, two possible values exist:
        - ``column`` (vertical alignment)
        - ``row`` (horizontal alignment).

Style
.....

.. _Color:

**Color**

.. tip::

    Try using `bootstrap colors <https://getbootstrap.com/docs/5.0/utilities/colors/>`_ instead.

``background_color``
    *Description*: With this attribute, one can define the background color of the element.

    *Values*: Color

``foreground_color``
    *Description*: With this attribute, one can set the foreground color of the element.

    *Values*: Color

``border_color``
    *Description*: With this attribute, one may set the border color.

    *Values*: Color

``on_hover``
    *Description*: With this attribute, one can enable or disable on-hover features for the element.

    *Values*: For the boolean type, either true or false are allowed - either as a string or as a Clingo symbol. If provided as a string, it is case-insensitive.

``on_hover_background_color``
    *Description*: With this attribute, one can set the background color of the element when on_hover is enabled.

    *Values*: Color

``on_hover_foreground_color``
    *Description*: With this attribute, one can set the foreground color of the element when on_hover is enabled.

    *Values*: Color

``on_hover_border_color``
    *Description*: With this attribute, one can set the border color of the element when on_hover is enabled.

    *Values*: Color

.. _Size:

.. tip::

    Try using `bootstrap size classes <https://getbootstrap.com/docs/5.0/utilities/sizing/>`_ instead.

**Size**

``height``
    *Description*: With this attribute, one can set the height in pixels of the element.

    *Values*: Integer

``width``
    *Description*: With this attribute, one can set the width in pixels of the element.

    *Values*: Integer

.. _Border:

**Border**

.. tip::

    Try using `bootstrap borders <https://getbootstrap.com/docs/5.0/utilities/borders/>`_ instead.

``border_width``
    *Description*: With this attribute, one defines the width of the border in pixels.

    *Values*: Integer

``border_color``
    *Description*: With this attribute, one may set the border color.

    *Values*: Color

.. _Visibility:

**Visibility**

``visibility``
    *Description*: Sets the visibility of an element. It can be used to show things like a modal or a container using the update functionality.

    *Values*: The visibility options are:
        - ``shown``: To show the element
        - ``hidden``: To hide the element

.. _Text:

**Text**

.. tip::

    Try using `bootstrap text <https://getbootstrap.com/docs/5.0/utilities/text/>`_ style instead.


Drag and Drop
.............

.. _Drag:

**Drag**


``draggable_as``
    *Description*: This attribute states that the element is draggable. Moreover, the value of this attribute is the data that will be passed to the drop event.
    This value will replace the placeholder ``_dragged`` which can appear in a ``when`` predicate.

    *Values*: Atom

``drop_target``
    *Description*: The values passed in this attribute are the possible target-elements where the current element can be dropped. The value must be the identifier of the target element.
    The dragged element will only be allowed to be dropped on the elements specified in this attribute.

    *Values*: Atom

.. admonition:: Example

    * A more elaborate example can be found in :ref:`Knapsack <Knapsack>`.

    Element  ``a`` can be dragged into elements ``b`` and ``c``. When ``a`` is dropped into ``b``, the assumption ``use(a)`` is added with the value ``true``.
    When ``a`` is dropped into ``c``, the assumption ``use(a)`` is added with the value ``false``.

    .. code-block::

        elem((a;b;c), container, w).
        attr(a, draggable_as, a).
        attr(a, drop_target, b).
        attr(a, drop_target, c).
        when(b, drop, call, add_assumption(use(_dragged),true)).
        when(c, drop, call, add_assumption(use(_dragged),false)).

