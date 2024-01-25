# Changelog

## v1.2.0 (Touchdesigner 2023.xx compatible)

### BACKWARD COMPATIBILTY

Due to major changes in Touchdesigner 2023.xx builds, this version does not support old Touchdesigner builds (before 2023.xx), but you can recall all of your presets and functions created in the previous versions of Pixel Wrangle

### IMPROVEMENTS

- Use the new Relative path workflow for TOX components
- Use Text file in sync mode for all external source code files

### BUGFIXES

- Remove old workaround cache nodes due to a bug in 2022 builds that cook each frame inside comp even without time dependency
- Fix script errors due to par name updates in GLSLMultiTOP in 2023 builds

### DEPENDENCIES

- Lygia updated to the current main branch (1.2.0)

## v1.1.3-rc2

### NEW FEATURES

- Added Instance manager Panel (browse all Pixel Wrangle exported instances in the project, reload in editor with double click, open parameters, viewers, network)
- Added instance linking (Track currently selected instance and load it automatically in the main UI to edit)
- Added macros allowing to switch between Compute and Vertex/Pixel shader modes on the fly without editing code (see help/readWrite preset for usage)
- Added miu_lab utilities functions for basic raymarching (ray and light structs, shadow, ao, normals, uniform fog)
- Added miu_lab noise functions (FBM, FastNoiseLite)
- Added raymarching presets based on miu_lab utilities functions
- Added pin instance CTRL L - pin parameter/viewer - code CTRL SHIFT L
- Added layout mode in viewer to check all buffers in single viewer

### IMPROVEMENTS

- Global UI improvements (add header bar, auto layout parameter pane, layout mode in viewer panes, pins, etc.)
- Allow single Pixel Wrangle OP manipulate multiple nodes (called 'Instances')
- Added storage in /storage. Pixel Wrangle is now an external tox that reload at startup
- Allow drag and drop previously exported instance in UI to reload it using op storage
- Recalling an instance will keep all parameter values as they are tuned in the instance
- When Pixel Wrangle is linked to an instance : Feed instance inputs as inputs fallback in main UI
- Improved autofocus current OP in parameter pane (contextual edit viewer, node type hints : blue = Pixel Wrangle Master, green = Pixel Wrangle instance, grey= regular OP)
- Edit node name in parameter pane
- Move build lib and export icons in header
- Move resolution, mode, etc. icons on the right
- Updated Macros and presets to use the new write() function macro
- Updated help presets

### BUGFIXES

- Include lygia readme and license in imported libraries
- Fixed pane w/h min size
- Fixed string expression properties in IO tab
- Fixed some sticky keyboard shortcuts

## v1.0.2-rc1

### NEW FEATURES

- Compute shaders, 2D array buffers, and 3D are all supported, with 100% functional parity with GLSLMultiTOP.
- All GLSL TOP parameter types are now supported, with an additional "Header" type parameter to aid in parameter layout in the Controls page.
- All parameter properties are available for customizing appearance.
- Ability to save your own functions/snippets to build your custom GLSL library.
- External library auto-parser to convert any arbitrary GLSL library (in the "Functions/dist" folder of the Pixel-Wrangle root) to a TD-compatible GLSL library (correcting paths and old syntaxes).
- One-click to parse and import all external libraries in your project (with static path resolving).
- One-click to export your shader in a new PanelCOMP (removing the Pixel-Wrangle dependency).
- The UI has been completely rebuilt, allowing you to customize the main background color, text size, text font, and text line height.
- Built-in mouse interactions are available everywhere while hovering a viewer and holding the [CTRL] key.
- A variety of macros have been added for common operations.
- Fuzzy search (and path-based) to find relevant functions and presets.

### IMPROVEMENTS

- All Pixel-Wrangle related data has been moved to a USER folder (Documents/Pixel-Wrangle) including vscode environment, cached code panes, saved presets and functions, and macros.
- The function loader now has preview hints (documentation headers and signatures)
- Keyboard shortcuts have been updated
- All parameters have hover-over help when the ALT key is held down
- Most of the UI elements have help message on hovering
- Non-default parameters are now always saved with presets (including resolution, bit depth, shader mode, etc.)
- Integration with Visual Studio Code has been improved and is now more stable
- The official documentation and Lygia are both integrated as submodules, see the installation instructions for more information.
- Crashes are now extremely rare.

### KNOWN BUGS

- Loading presets is still buggy, you may need to load them twice.
- Most keybindings are slightly sticky (but still usable).
- Releasing the [CTRL] key after an interaction in the parameter pane viewer will reset the mouse position to the last main viewer position.
- Navigation in the presets and functions browser with arrow keys does not allow you to press and hold to scroll through the list, and the left arrow key collapses all opened directories (so, it is recommended to use your mouse instead).
- Some cacheTOP in subnet may cook unnecessarily after loading a preset. Toggling the time dependency generally solves the problem.
