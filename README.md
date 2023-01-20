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

# Quick Install

- Clone the repo with all the submodules at root of your Palette folder located in Documents/Derivative

```bash
git clone -b dev --recurse-submodules https://github.com/miu-lab/Pixel-Wrangle.git
```

- Update your Palette
