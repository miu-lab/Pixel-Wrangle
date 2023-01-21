![thumb](https://user-images.githubusercontent.com/97438154/213440174-e47382e6-5281-4fab-b82c-a77fd6babb52.png)

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
- One-click export of your shader as a standard GLSL network, eliminating framework dependency

This project is heavily inspired by the VEX Wranglers in the Houdini ecosystem.

You can find the official "work-in-progress" documentation at the following [link](https://miu-lab.github.io/Pixel-Wrangle-doc) (available in both English and French)

# Changelog

## **2023-01-21** -> Pixel-Wrangle - Pre-release - RC1

**Please note that this is the first release candidate and it may contain unknown bugs. Use it for your projects at your own risk.**

*Tests were run on a Windows system, an AMD CPU, an RTX 3XXX GPU, and the latest version of TouchDesigner 2022.* If you encounter any critical bugs, please let us know in the issues section of the repository.

The [documentation](https://miu-lab.github.io/Pixel-Wrangle-doc/) is currently in a 'work in progress' state and will be updated soon. It will be available in both French and English.

## Features

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

## Improvements

- All Pixel-Wrangle related data has been moved to a USER folder (Documents/Pixel-Wrangle) including vscode environment, cached code panes, saved presets and functions, and macros.
- The function loader now has preview hints (documentation headers and signatures)
- Keyboard shortcuts have been updated
- All parameters have hover-over help when the ALT key is held down
- Most of the UI elements have help message on hovering
- Non-default parameters are now always saved with presets (including resolution, bit depth, shader mode, etc.)
- Integration with Visual Studio Code has been improved and is now more stable
- The official documentation and Lygia are both integrated as submodules, see the installation instructions for more information.
- Crashes are now extremely rare.

## Known bugs

- Loading presets is still buggy, you may need to load them twice.
- Most keybindings are slightly sticky (but still usable).
- Releasing the [CTRL] key after an interaction in the parameter pane viewer will reset the mouse position to the last main viewer position.
- Navigation in the presets and functions browser with arrow keys does not allow you to press and hold to scroll through the list, and the left arrow key collapses all opened directories (so, it is recommended to use your mouse instead).
- Some cacheTOP in subnet may cook unnecessarily after loading a preset. Toggling the time dependency generally solves the problem.

## **Quick Install**

### Requirements

- [TouchDesigner 2022.29530 or later](https://derivative.ca/download)
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
