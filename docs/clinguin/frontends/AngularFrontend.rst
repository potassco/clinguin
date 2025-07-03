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

``sidebar``
..............

A sidebar panel that slides in from the edge of the screen, triggered by hovering near the edge and can be pinned to remain visible.

The elements in the sidebar can't be ordered directly, to impose an order one can crate a main container and set the order of the container.

**Attributes**

:ref:`Class <Class>`,

``title``
    *Description*: The title displayed at the top of the offcanvas panel. It is optional.

    *Values*: String

``position``
    *Description*: The side of the screen from which the offcanvas appears

    *Values*: String. Can be ``start`` (left side) or ``end`` (right side). Defaults to ``start``.


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


``tabs``
.................

The tabs element creates a tabbed interface, allowing users to organize content into separate panes that can be viewed by clicking on corresponding tab buttons. Tabs are useful for grouping related content while conserving screen space. All children should be :ref:`tabs-item`

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

``orientation``
    *Description*: Determines whether tabs are displayed horizontally or vertically.

    *Values*: String. Can be `horizontal`` (default) or `vertical`.

The `class` attribute can be used with the following custom classes for styling:

- `nav-tabs`: Displays tabs with a tab-like appearance (default)
- `nav-pills`: Displays tabs with a button-like appearance
- `nav-fill`: Makes tabs fill the available width equally

``tabs-item``
.................

A child element of `tabs` that represents an individual tab and its content.

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`

``title``
    *Description*: The text displayed on the tab button.

    *Values*: String.

``active_class``
    *Description*: Bootstrap classes to apply to the tab button when it is active.

    *Values*: String or list of strings.

``inactive_class``
    *Description*: Bootstrap classes to apply to the tab button when it is inactive.

    *Values*: String or list of strings.


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

``file_input``
...................

A file input component that allows users to upload files to the backend.
These files are not automatically activated, they need to be activated using the `activate_file` operation.
When a file is chosen the event `change` is triggered, with this, the file name and content (in base 64) are added to the context,
then, the corresponding `when` events are triggered.
When allowing multiple selection of files, all `when` events will be processed for each file separate.

**Attributes**
:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`

``accept``
	*Description*: The file types that are accepted for upload. This attribute is optional and defaults to ".lp" files.

	*Values*: String. Can be a list of file extensions (e.g., ".lp" for ASP files or ".txt" for text files)

``disabled``
	*Description*: Disables the file input field.

	*Values*: Boolean (`true` to disable, `false` to enable). Default is `false`.

``multiple``
	*Description*: Allows uploading multiple files at once. Each file will pre processed by an individual operation execution.

	*Values*: Boolean (`true` to disable, `false` to enable). Default is `false`.

.. admonition:: Example

	``file_input`` works with the ``upload_file`` operation.

	.. code-block:: prolog

		elem(file_input, file_input, main_container).
		attr(file_input, accept, ".lp").
		when(file_input, change, call, upload_file(_value)).

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


``collapse``
.............

A collapsible element. Corresponds to a limited version of `Bootstrap collapse <https://getbootstrap.com/docs/5.0/components/collapse/>`_.
It behaves like a normal button that will show and hide content when clicked. Unlike the usual button, ``collapse`` can contain other elements, similarly to the ``container``.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Child layout <Child layout>`,
:ref:`Direction <Direction>`,

``collapsed``
	*Description*: The initial state of the collapse

	*Values*: Boolean (`true` for collapsed, `false` for expanded)

``label``
	*Description*: The label of the collapse

	*Values*: String

``icon``
	*Description*: The icon of the button.

	*Values*: `Font Awesome <https://fontawesome.com/search?o=r&m=free>`_ symbol name


.. important::
	**Child Elements**

	All elements intended to appear inside the `collapse` component **must** be defined as its children. These can include any UI element.

.. warning::
	**Automatic close**

	The `collapse` component will go back to its original state ("collapsed" or "expanded") after every call to the server


.. admonition:: Example

    In this example a ``collapse`` component ``c`` contains a button ``b1`` as its child.
    The component toggles between expanded and collapsed states when the user interacts with it.

	.. code-block:: prolog

		elem(c, colapse, w).
		attr(c, label, "Collapse").
		elem(b1, button, c).



``line``
.............

A line between two element. The line is created using the `LeaderLine <https://anseki.github.io/leader-line/#options>`_ tool.
It can be used to add a visual connection between two elements in the UI.
All the attributes of the `LeaderLine` can be used to customize the appearance and behavior of the line, check their documentation for more details.

**Attributes**

:ref:`Class <Class>`,
:ref:`Visibility <Visibility>`,
:ref:`Order <Order>`,
:ref:`Child layout <Child layout>`,
:ref:`Direction <Direction>`,

``start``
	*Description*: The element where the line starts.

	*Values*: The identifier of the element

``end``
    *Description*: The element where the line ends.

    *Values*: The identifier of the element

``color``
    *Description*: The color of the line.
    *Values*: Color. Can be a color name (e.g., "red", "blue") or a hex code (e.g., "#FF0000", "#0052CC"). Defaults to "#0052CC". Use ``@color`` directive to use the color pallet for clinguin.

``size``
    *Description*: The size of the line.
    *Values*: Integer. Defaults to 2.

``path``
    *Description*: The path of the line. It can be "arc", "straight", or "fluid".
    *Values*: String. Defaults to "arc".

``startSocket``
    *Description*: The identifier of the starting socket for the line.
    *Values*: String. Defaults to "".

``endSocket``
    *Description*: The identifier of the ending socket for the line.
    *Values*: String. Defaults to "".

``startSocketGravity``
    *Description*: The gravity or pull at the starting socket, affecting line curvature.
    *Values*: Number. Defaults to 0.

``endSocketGravity``
    *Description*: The gravity or pull at the ending socket, affecting line curvature.
    *Values*: Number. Defaults to 0.

``startPlug``
    *Description*: The type of plug at the start of the line.
    *Values*: String. Defaults to "".

``endPlug``
    *Description*: The type of plug at the end of the line.
    *Values*: String. Defaults to "".

``startPlugColor``
    *Description*: The color of the plug at the start of the line.
    *Values*: String representing a color code. Defaults to "".

``endPlugColor``
    *Description*: The color of the plug at the end of the line.
    *Values*: String representing a color code. Defaults to "".

``startPlugSize``
    *Description*: The size of the plug at the start of the line.
    *Values*: Number. Defaults to 2.

``endPlugSize``
    *Description*: The size of the plug at the end of the line.
    *Values*: Number. Defaults to 2.

``outline``
    *Description*: Whether the line has an outline.
    *Values*: Boolean. Defaults to false.

``outlineColor``
    *Description*: The color of the line's outline.
    *Values*: String representing a color code. Defaults to "".

``outlineSize``
    *Description*: The thickness of the line's outline.
    *Values*: Number. Defaults to 1.

``startPlugOutline``
    *Description*: Whether the start plug has an outline.
    *Values*: Boolean. Defaults to false.

``endPlugOutline``
    *Description*: Whether the end plug has an outline.
    *Values*: Boolean. Defaults to false.

``startPlugOutlineSize``
    *Description*: The thickness of the outline for the start plug.
    *Values*: Number. Defaults to 1.

``endPlugOutlineSize``
    *Description*: The thickness of the outline for the end plug.
    *Values*: Number. Defaults to 1.

``startPlugOutlineColor``
    *Description*: The color of the outline for the start plug.
    *Values*: String representing a color code. Defaults to "".

``endPlugOutlineColor``
    *Description*: The color of the outline for the end plug.
    *Values*: String representing a color code. Defaults to "".

``startLabel``
    *Description*: The label displayed at the start of the line.
    *Values*: String. Defaults to "".

``endLabel``
    *Description*: The label displayed at the end of the line.
    *Values*: String. Defaults to "".

``middleLabel``
    *Description*: The label displayed in the middle of the line.
    *Values*: String. Defaults to "".

``dash``
    *Description*: Whether the line is dashed.
    *Values*: Boolean. Defaults to false.

``gradient``
    *Description*: Whether the line uses a gradient color.
    *Values*: Boolean. Defaults to false.

``dropShadow``
    *Description*: Whether the line has a drop shadow effect.
    *Values*: Boolean. Defaults to false.





.. important::
	**Loops**

	The start and end elements of the line must be different.


.. admonition:: Example

    In this example a ``line`` between button ``b1`` and button ``b2``. In this case we use ``@color(blue)`` to set the color of the line using the `@color` directive
    from the :ref:`ClingraphContext`.

	.. code-block:: prolog

		elem(b1, button, w).
		elem(b2, button, w).
		elem(l, line, w).
        attr(l, start, b1).
        attr(l, end, b2).
		elem(b1, color, @color(blue)).



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


.. admonition:: **Calculating dragging targets**
    :class: important

    In some cases, the possible targets for a draggable elements want to be obtained from ``_any/2``.
    These atoms, however, might not be available because of the restrictions imposed by previous selections (assumptions).
    When this is the case. An intermediate call can be made to remove the assumptions and get the available targets using the ``_any/2`` predicate.
    This means one can add a lock/unlock button to the draggable elements which will remove the previous assumption to obtain the options while storing in the context the previous selection.

    .. admonition:: Example

        This example extends the Knapsack problem and with the following code:

        Make sure the line ``attr(object(O), draggable_as, O):-object(O, _).`` is commented out.

        .. code-block:: prolog

            % ---- Unlock to drag an object
            % This allows an intermediate call that will remove assumptions to get available destination using the _any/2 predicate


            % Unlocked objects will appear in the original column
            object(O, X):- object(O), _clinguin_context(unlocked(O),X).

            % Unlocked objects are draggable and stand out
            attr(object(O), filter, "opacity(0.8)"):-object(O), not _clinguin_context(unlocked(O),_).
            attr(object(O), "box-shadow", "0 2px 2px 2px #00000070" ):- object(O), _clinguin_context(unlocked(O),_).
            attr(object(O), draggable_as, O):-object(O, _), _clinguin_context(unlocked(O),_).

            % Button to lock and unlock objects
            elem(object_move(O), button, object(O)):-object(O,_).
            attr(object_move(O), icon, "fa-lock"):-object(O,_), not _clinguin_context(unlocked(O),_).
            attr(object_move(O), icon, "fa-lock-open"):-_clinguin_context(unlocked(O),_).
            attr(object_move(O), class, ("btn-sm";"btn-outline-primary";"border"; "border-0")):-object(O,_).
            % When unlocking the assumption is removed and the context is updated
            when(object_move(O), click, call, remove_assumption(take(O))):-object(O, _), not _clinguin_context(unlocked(O),_).
            when(object_move(O), click, context, (unlocked(O),X)):-object(O, X), not _clinguin_context(unlocked(O),_).

            % Dummy event for locking an object
            when(object_move(O), click, call, get):-_clinguin_context(unlocked(O),_).

            % Any action, if something was unlocked then it is put back
            when(O', E, call, get):- when(O', E, call, _), E!=drop, _clinguin_context(unlocked(O),available).
            when(O', E, call, add_assumption(take(O),true)):- when(O', E, call, _), E!=drop, _clinguin_context(unlocked(O),taken).
            when(O', E, call, add_assumption(take(O),false)):- when(O', E, call, _), E!=drop, _clinguin_context(unlocked(O),not_available).
