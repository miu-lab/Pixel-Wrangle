/* Pixel Wrangle - BUILTIN UNIFORMS */

// From TD 
uniform vec3 Time;          // x : Time in seconds, y : Time in frames, z : 1/FPS
uniform vec4 MousePos;      // xy : normalized position (LMB DOWN), zw : normalized position 
uniform vec4 MouseClicks;   // x : ANY Mouse button pressed, y: LMB pressed, z: MMB pressed, w: RMB pressed
uniform vec4 MouseDeltaLMB; // xy : LMB Position - Current Mouse Position, zw : Relative Position (LMB Down)
uniform vec4 MouseDeltaMMB; // xy : MMB Position - Current Mouse Position, zw : Relative Position (MMB Down)
uniform vec4 MouseDeltaRMB; // xy : RMB Position - Current Mouse Position, zw : Relative Position (RMB Down)
uniform vec2 MouseWheel;    // [Mouse Wheel Value, Mouse Wheel Slope]
uniform vec2 MouseSlope;    // Mouse Slope


// Shadertoy uniforms
uniform vec2 iResolution;   // Resolution in pixels
uniform float iTime;        // Time in seconds
uniform float iTimeDelta;   // 1/FPS
uniform float iFrameRate;   // FPS
uniform float iFrame;       // Time in frames
uniform vec4 iMouse;        // xy : normalized position (LMB DOWN), zw : normalized position 