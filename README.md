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

## **Quick Install**

### Requirements

- [TouchDesigner 2023.11340 or later](https://derivative.ca/download)
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
