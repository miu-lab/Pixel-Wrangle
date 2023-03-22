# Changelog

## v1.01-rc2

- Added storage in /storage. Pixel Wrangle is now an external tox that reload at startup
- Allow single Pixel Wrangle OP manipulate multiple nodes (called 'Instances')
- Added Instance manager Panel (browse all Pixel Wrangle exported instances in the project, reload in editor with double click, open parameters, viewers, network)
- Global UI improvements (add header bar, auto layout parameter pane, layout mode in viewer panes, pins, etc.)
- Improved autofocus current OP in parameter pane (contextual edit viewer, node type hints : blue = Pixel Wrangle Master, green = Pixel Wrangle instance, grey= regular OP)
- Allow drag and drop previously exported instance in UI to reload it using op storage
- Recalling an instance will keep all parameter values as they are tuned in the instance
- Added instance linking (Track currently selected instance and load it automatically in the main UI to modify it)
- When Pixel Wrangle is linked to an instance : Feed instance inputs as inputs fallback in main UI
- Added macros allowing to switch between Compute and Vertex/Pixel shader modes on the fly without editing code (see help/readWrite preset for usage)
- Updated Macros and presets to use the new write() function macro
- Updated help presets
- Added miu_lab utilities functions for basic raymarching (ray and light structs, shadow, ao, normals, uniform fog)
- Added miu_lab noise functions (FBM, FastNoiseLite)
- Added raymarching presets based on miu_lab utilities functions
- Fixed pane w/h min size
- Fixed string expression properties in IO tab
- Fixed some sticky keyboard shortcuts
- Include lygia readme and license in imported libraries
- Added pin instance CTRL L - pin parameter/viewer - code CTRL SHIFT L
- Edit node name in parameter pane
- Added layout mode in viewer to check all buffers in single viewer
- Move build lib and export icons in header
- Move resolution, mode, etc. icons on the right
