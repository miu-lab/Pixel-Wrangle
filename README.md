<img width="1920" alt="image" src="https://user-images.githubusercontent.com/97438154/194752652-c05127ac-6bf9-4197-bc13-9e4326845634.png">

# Pixel Wrangle

> Pixel Wrangle is a Touchdesigner TOX that acts like a wrapper for GLSL TOP,  
It’s built for quick prototyping GLSL in Touchdesigner. 
> 

This project is widely inspired by the VEX Wranglers in the Houdini eco-system.
It provides auto-parameter generation for uniforms, as standard Touchdesigner parms, and more...
You can save and reload presets on demand.

Some 'starter' presets are provided as proof of concept.

This includes the last implementations of FastNoiseLite 2D and 3D (OpenSimplex, Perlin, Cellular…) in GLSL that are really good quality and reasonably fast in comparison with regular Noise TOP.


### **Philosophy**

- Quick Auto generated UI by declaration in your code (with range and default values)
- Minimal overheads (static updates for most)
- Built-in Touchdesigner UI, allows you to easily map it from external, use expressions, etc..
- Functional parity with GLSL TOP (in progress)


### Good to know :

- UI and panes are all vector and resizable.
- You can plug 8 Ins / 8 Outs as Texture Buffers
- You can bypass ‘uniform’ keyword in your code.
- Only [Controls, Inputs, Outputs] pages are saved in your preset but you can include any custom parameter in your preset by adding it directly from component editor in [Controls] Page. All other pages are ignored.
- All parameters are generated as float or vector of float, you can cast it to int in your code, and/or change parameter type to int in component editors. Changes are saved with preset.
- Outputs are generated and activated by declaration in your code but you can modify it manually in Outputs Tab
- Inputs as texture buffer are manually settable via Inputs Tab and referenced by integer as GLSL TOP do it.
- Ability to activate Auto-focus in parameter pane, to display parm of any 'Current' node. Easy tweak other OPs parameters, keeping main viewer active.

### Current Limitations :

- For now, parameter generation only works with uniforms. Array types, matrices, and atomic counters are not supported yet

### Known bugs :

- **Loading preset is buggy, you sometimes have to click multiple times to load custom parameters properly**
- Parameter order can be a bit erratic when you change order in your declarations, so be aware of that.
- On dropping node, init state don't show you code panels, you have to refresh it by opening viewer and click tabs to display it properly
- [TD Limitation] Panels are not resized properly as long as you visualize it directly in node UI. But you can open viewer then everything in UI is updating properly
- [TD Limitation] Parameter pane don’t always display updates when you load preset, you may have to reload the viewer
- [TD Limitation] Execute code by pressing [CTRL] + Enter will lose text cursor position

### Keyboard Shortcuts :

**On OP is current in Network** →

- [CTRL] + Enter : Open Viewer

**Everywhere in the OP Viewer** →

- [CTRL] + Enter : Execute
- Escape         : Close viewer
- [CTRL] + P     : Toggle display of Parameter pane
- [CTRL] + 0     : Toggle display of Viewer pane tabs (in Parameter pane)
- [CTRL] + 9     : Toggle display of [READ-ONLY] Full code output 

**On Main Panel only** →

- [CTRL] + 1     : Toggle display of IO Panel
- [CTRL] + 2     : Toggle display of Functions Panel
- And all the same builtins interaction than regular TOPs and DATs (OP Viewer)

### Syntax specifics :

IO Panel **ONLY** →

```glsl
float Foo; // min=-1 max=1 default=0
vec3 Bar; // mode=c default=[1,1,0]
```

- No more 'uniform' keyword, but you can leave it if you prefer
- Parameter settings with inline comments + ' ', then property=value, space-separated.
- Currently available properties : 'mode', 'min', 'max', 'default'
- Mode defines parameter mode like 'vector' or 'color' // 'mode' values : 'c' OR 'v' eg: '// mode=c' to generate a parameter in color mode.
- 'mode=c' only works on 'vec3' or 'vec4'
- Set default values on 'float' - eg: 'default=0' to set black
- Set default values on 'vec*' - eg with 'vec3': 'default=0' -> black, 'default=[1]' -> red, 'default=[1, 0, 1]' -> magenta
- If you specify nothing, default values are used -> mode=v min=0 max=1 default=0.5

## For now this version still in Beta and free access

Depending on the feedbacks there could be a full version in the coming months. 
At this stage I am listening to any proposal for improvement and will read all the RFEs.
I will do my best to answer it.

**Future versions would have:**

- Full parity with GLSL TOP (compute shaders, all parameter types, 3D)
- Internal feedbacks, better buffer management
- A wider list of presets
- A preset browser with metadata( eg: category, tags ) callable with tab-like menu
- A basic form of inline snippet loader to load most used functions

## Quick Installation

- Clone or dowmload and extract zip content in your User palette, located in Documents/Derivative/Palette
<img width="383" alt="image" src="https://user-images.githubusercontent.com/97438154/194753006-2f26c8cd-5474-4177-a52c-9f57373f76f8.png">

- Update your palette
<img width="226" alt="palette" src="https://user-images.githubusercontent.com/97438154/194753342-c1614d33-9f1c-4987-b012-63685e6b49cd.png">

- Drop node in network, press [CTRL] + Enter to open viewer
- <img width="240" alt="image" src="https://user-images.githubusercontent.com/97438154/194758085-8eb29a36-5fc5-4d85-980b-9e0183806831.png">

