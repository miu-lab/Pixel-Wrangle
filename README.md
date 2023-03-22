![image](https://user-images.githubusercontent.com/97438154/226935988-b20ef615-6295-4836-828b-64a16d27c9f7.png)

# Pixel Wrangle

> Pixel Wrangle is a minimalist GLSL framework built on top of GLSL TOP.
> This is delivered as .tox component that allows you to quick prototyping GLSL in Touchdesigner.

## **Philosophy and main features**

- Functional parity with GLSL TOP
- A user interface that is as simple, pleasant, and straightforward as possible
- Dynamically generated TouchDesigner parameters by declaring uniforms (with customizable properties)
- Minimal CPU overhead
- Easy use, creation, and management of your own libraries of presets and functions
- One-click auto-parsing and importing of third-party libraries (Lygia is fully integrated)
- One-click export of your shader as a standard GLSL network, eliminating framework dependency (called 'Instance')

This project is heavily inspired by the VEX Wranglers in the Houdini ecosystem.

You can find the official "work-in-progress" documentation at the following [link](https://miu-lab.github.io/Pixel-Wrangle-doc) (available in both English and French)

# Changelog

## **2023-03-22** -> Pixel-Wrangle - Pre-release - RC2

**Please note that release candidate may contain unknown bugs. Use it for your projects at your own risk.**

*Tests were run on a Windows system, an AMD CPU, an RTX 3XXX GPU, and the latest version of TouchDesigner 2022.* If you encounter any critical bugs, please let us know in the issues section of the repository.

The [documentation](https://miu-lab.github.io/Pixel-Wrangle-doc/) is currently in a 'work in progress' state and will be updated soon. It will be available in both French and English.

## Features

- Added Instance manager Panel (browse all Pixel Wrangle exported instances in the project, reload in editor with double click, open parameters, viewers, network)
- Added instance linking (Track currently selected instance and load it automatically in the main UI to edit)
- Added macros allowing to switch between Compute and Vertex/Pixel shader modes on the fly without editing code (see help/readWrite preset for usage)
- Added miu_lab utilities functions for basic raymarching (ray and light structs, shadow, ao, normals, uniform fog)
- Added miu_lab noise functions (FBM, FastNoiseLite)
- Added raymarching presets based on miu_lab utilities functions
- Added pin instance CTRL L - pin parameter/viewer - code CTRL SHIFT L
- Added layout mode in viewer to check all buffers in single viewer

## Improvements

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

## Bug Fixes

- Include lygia readme and license in imported libraries
- Fixed pane w/h min size
- Fixed string expression properties in IO tab
- Fixed some sticky keyboard shortcuts

## **Quick Install**

### Requirements

- [TouchDesigner 2022.32120 or later](https://derivative.ca/download)
- [Git](https://git-scm.com/downloads)

### Installation

#### Manual

- Use Git to clone the repository with all its submodules at the root of your Palette folder located in ocuments/Derivative

```bash
git clone --recurse-submodules https://github.com/miu-lab/Pixel-Wrangle.git
```

- Update your Palette

#### Automatic

- Download and execute setup.sh (with Git Bash) provided in the [Release section](https://github.com/miu-lab/Pixel-Wrangle/releases)
- Update your Palette
