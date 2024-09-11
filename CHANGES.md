# Changes

## clinguin 2.0.1

  * Bug fix
    * Message elements now on top
  * Docs
    * Added documentation for mouse events

## clinguin 2.0.0


  * Incompatible
    * `_clinguin_assume/1` is now `_clinguin_assume/2` where the second argument is either `true` or `false`
    * Operation `add_assumption/1` is now `add_assumption/2` where the second argument is either `true` or `false`
    * `ClingoMultishotBackend` is now subsumed by `ClingoBackend`

  * Additions
    * Backend extension
      * instead of extending `__init__` now initializations are separated
      * added attribute `self._args`
      * ExplanationBackend now using `clingexplaid` library
    * Operations
      * added operation to ground
      * added option to set false assumptions
      * type parsing and defaults for user input in `_context_value`
      * model selection now accepts show statements for filtering
      * added operation to set a constant
    * Attributes
      * Attribute `visible` is now `visibility` and the values are either `shown` or `hidden`
      * Attribute regarding style (such as `filter`) for canvas elements with an image path are now applied only to the canvas
    * Components
      * New component `progress_bar`
      * New component `checkbox`
    * Domain constructors
      * added optimization information into domain state
      * added information about externals
      * added automatic check to skip constructors based on `ui files`
      * added information about the constants
    * Examples
      * New example with incremental solving
      * New examples with optimization and false assumptions
    * UI
      * Loader while server responds
    * Command line
      * added command line option for optimization timeout
      * added argument for clingo general command line arguments
    * General documentation update!


  Note: Make sure you clear your browsers cache to ensure it uses the latest version


