<img width="1920" alt="image" src="https://user-images.githubusercontent.com/97438154/194752652-c05127ac-6bf9-4197-bc13-9e4326845634.png">

# Pixel Wrangle

> Pixel Wrangle is a GLSL TOP wrapper built for quick prototyping GLSL in Touchdesigner

## **Philosophy**

- Quick Auto generated UI by declaration in your code (with range and default values)
- Minimal overheads (static updates for most)
- Built-in Touchdesigner UI, allows you to easily map it from external, use expressions, etc..
- Functional parity with GLSL TOP (in progress)

This project is widely inspired by the VEX Wranglers in the Houdini eco-system.
It provides auto-parameter generation for uniforms, as standard Touchdesigner parms, and more...
You can create and reload your own presets.
Some 'starter' presets are provided as proof of concept, including the last implementations of FastNoiseLite 2D and 3D (OpenSimplex, Perlin, Cellular…) in GLSL that are really good quality and reasonably fast in comparison with regular Noise TOP.

## **Good to know**

- UI and panes are all vector and resizable.
- Currently, only tested on Touchdesigner 2022.26590,. Due to use of the new Text COMP, 2021.XX versions may be problematic.
- You can plug 8 Ins / 8 Outs as Texture Buffers
- You can bypass ‘uniform’ keyword in your code.
- Only [Controls, Inputs, Outputs] pages are saved in your preset but you can include any custom parameter in your preset by adding it directly from component editor in [Controls] Page. All other pages are ignored.
- All parameters are generated as float or vector of float, you can cast it to int in your code, and/or change parameter type to int in component editors. Changes are saved with preset.
- Outputs are generated and activated by declaration in your code but you can modify it manually in Outputs Tab
- Inputs as texture buffer are manually settable via Inputs Tab and referenced by integer as GLSL TOP do it.
- Ability to activate Auto-focus in parameter pane, to display parm of any 'Current' node. For easy tweaking other OPs parameters, keeping main viewer active.
- Screen resolution is the only pre-declared 2D uniform, called 'uRes'
- Built-in feedback system

## **Current limitations**

- For now, parameter generation only works with uniforms.
- Matrix, array buffers and atomic counters are not currently supported
- Compute shaders and 3D are not currently supported

## **Known bugs**

- Loading preset is buggy, you sometimes have to click multiple times to load custom parameters properly
- Parameter order can be a bit erratic when you change order in your declarations, so be aware of that.
- On dropping node, init state doesn't show you the code panels, you have to refresh it by opening viewer and click tabs to display properly
- A bit of random crashes...
- [TD Limitation] Panels are not resized properly as long as you visualize it directly in node UI. But you can open viewer then everything in UI is updating properly
- [TD Limitation] Parameter pane don’t always display updates when you load preset, you may have to reload the viewer
- [TD Limitation] Execute code by pressing [CTRL] + Enter will lose text cursor position

## **Keyboard shortcuts**

### **If OP is "current" in network view** →

- **[CTRL]** + **Enter** : Open Viewer
- **[CTRL]** + **E** : Open VS Code

### **In the OP viewer** →

- **[CTRL]** + **Enter** : Execute
- **Escape** : Close viewer
- **[CTRL]** + **E** : Open VS Code
- **[CTRL]** + **P** : Toggle display of Parameter pane
- **[CTRL]** + **0** : Toggle display of Viewer pane tabs (in Parameter pane)
- **[CTRL]** + **9** : Toggle display of [READ-ONLY] Full code output

### **On main panel only** →

- **[CTRL]** + **1** : Toggle display of IO Panel
- **[CTRL]** + **2** : Toggle display of Functions Panel
- All the same builtins interaction than regular TOPs and DATs (OP Viewer)

## **Syntax specifics**

### IO PANEL **ONLY** →

```glsl
// IO Syntax declaration exemple
 
float Foo; // min=-1 max=1 default=0
vec3 Bar; // mode=c default=[1,1,0]
```

- No more 'uniform' keyword needed, but you can leave it if you are old-school
- Parameter settings with inline comments + ' ', then property=value, space-separated.
- Currently available properties : 'mode', 'min', 'max', 'default'
- Mode defines parameter mode like 'vector' or 'color' // 'mode' values : 'c' OR 'v' eg: '// mode=c' to generate a parameter in color mode.
- 'mode=c' only works on 'vec3' or 'vec4'
- Set default values on 'float' - eg: 'default=0' to set black
- Set default values on 'vec*' - eg with 'vec3': 'default=0' -> black, 'default=[1]' -> red, 'default=[1, 0, 1]' -> magenta
- If you specify nothing, default values are used -> mode=v min=0 max=1 default=0.5

## **For now, this version still beta and free access**

Depending on the feedbacks there could be a full version in the coming months.
At this stage I am listening to any proposal for improvements and will read all the RFEs.
I will do my best to answer it.

### Future versions would have

- Full parity with GLSL TOP (compute shaders, all parameter types, 3D)
- Better buffer management
- A wider list of presets
- A preset browser with metadata( eg: category, tags ) callable with tab-like menu
- A basic form of inline snippet loader to load most used functions

## **Quick start**

- Clone the repository or download and extract zip content in your User palette, located in Documents/Derivative/Palette\
<img width="33%" alt="image" src="https://user-images.githubusercontent.com/97438154/194753006-2f26c8cd-5474-4177-a52c-9f57373f76f8.png">

- Update your palette\
<img width="33%" alt="palette" src="https://user-images.githubusercontent.com/97438154/194753342-c1614d33-9f1c-4987-b012-63685e6b49cd.png">

- Drop node in network, press [CTRL] + Enter to open viewer\
<img width="33%" alt="image" src="https://user-images.githubusercontent.com/97438154/194758085-8eb29a36-5fc5-4d85-980b-9e0183806831.png">

## **Working with VS Code**

There is a keyboard shortcut [CTRL] + E to edit current shader in VS Code.

It will open a new instance of VS Code in a folder that contains all panels in 4 separate files.

Each of these folders are stored in the default 'touchtmp' folder.

The naming scheme is **\<TOUCHTMP\>**/**\<PROJECTNAME\>**/**\<OPID\>** with :

- **TOUCHTMP** = Touchdesigner temp folder path. Run 'var('TEMP')' in a python console to see yours
- **PROJECTNAME** = current project name without digits
- **OPID** = the unique ID of the current PixelWrangle OP

### **Prerequisites**

- [Download](https://code.visualstudio.com/download) and install VS Code on your machine
- Update path if necessary

### **Environment**

When you open VS Code editor for the first time, a brand new environment is created in your home folder -> C:/Users/\<**YourUserProfile**\>/.vscode-td/glsl

You will start with a clean environment.\
Default settings, no extensions.\
You can add your favorites.

Now, each time you will open VS Code on this 'OP type', it will load this specific environment.

For a quick start, you will find a very minimal code profile that you can import in your custom environment.\
It will download some usefull extensions to write glsl, and import TD specifics variables/functions for auto-completion engine.

You can just hit [CTRL] + P, run this commands and choose 'glsl.code-profile' provided at root of this repo.\
<img width="33%" alt="image" src="https://user-images.githubusercontent.com/97438154/197342847-dadb3698-e839-46b7-83eb-dc028688ac2e.png">
