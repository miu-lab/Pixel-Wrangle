// Constants
#define _PI 3.1415926535897932384626433832795                      // float _PI     = PI Value (3.14...)
#define _TAU _PI * 2                                               // float _TAU    = 2 * PI Value (7.28...)
#define _GOLD 1.618033988749894                                    // float _GOLD   = Golden Ratio (1.618...)
#define _E 2.7182818284590452353602874713527                       // float _E      = Euler Number

// Screen
#define _RES vec2(uTDOutputInfo.res.z,uTDOutputInfo.res.w)         // vec2  _RES     = 2D Resolution in Pixels
#define _DEPTH uTDOutputInfo.depth.y                               // float _DEPTH   = Depth
#define _RATIO2D vec2(max(_RES.x/_RES.y, 1),max(_RES.y/_RES.x, 1)) // vec2  _RATIO2D = Ratio from Max Axis
#define _CENTER 0.5                                                // float _CENTER  = Center

// 2D Position
#define _POS2DN vec2(_POS2D) / _RES+vec2((min(_RATIO2D, 1)*.5)/_RES) // vec2 _POS2DN   = 2D Normalized Position (vUV.st)
#define _POS2DC _POS2D - vec2(_RES/2)                                // vec2 _POS2DC   = 2D Centered Position in Pixels
#define _POS2DNC (vec2(_POS2D) / _RES - _CENTER)                     // vec2 _POS2DNC  = 2D Normalized + Centered Position
#define _POS2DNR _POS2DN * _RATIO2D                                  // vec2 _POS2DNC  = 2D Normalized + Ratio Position
#define _POS2DNCR (vec2(_RATIO2D) * vec2(_POS2DN - _CENTER))         // vec2 _POS2DNCR = 2D Normalized + Centered + Ratio Position

// 3D Position
#define _POS3DN vec3(_POS2DN,_DEPTH)                                // vec3 _POS3DN   = 3D Normalized Position (vUV.stp)
#define _POS3DC _POS3D - vec3(vec2(_RES/2), _DEPTH/2)               // vec3 _POS3DC   = 3D Centered Position in Pixels
#define _POS3DNC _POS3DN - _CENTER                                  // vec3 _POS3DNC  = 3D Normalized + Centered Position
#define _POS3DNR _POS3DN * vec3(_RATIO2D, 1/_DEPTH)                 // vec3 _POS3DNC  = 3D Normalized + Ratio Position
#define _POS3DNCR ( vec3(_RATIO2D, 1/_DEPTH) * (_POS3DN - _CENTER)) // vec3 _POS3DNCR = 3D Normalized + Centered + Ratio Position

// 2D Position Shortcuts
#define _UV _POS2D       // ivec2 _UV    = 2D Position in Pixels
#define _UVN _POS2DN     //  vec2 _UVN   = 2D Normalized Position (vUV.st)
#define _UVC _POS2DC     //  vec2 _UVC   = 2D Centered Position in Pixels
#define _UVNC _POS2DNC   //  vec2 _UVNC  = 2D Normalized + Centered Position
#define _UVNR _POS2DNR   //  vec2 _UVNR  = 2D Normalized + Ratio Position
#define _UVNCR _POS2DNCR //  vec2 _UVNCR = 2D Normalized + Centered + Ratio Position

// 3D Position shorctuts
#define _P _POS3D       // ivec3 _P    = 3D Position in Pixels
#define _PN _POS3DN     //  vec3 _PN   = 3D Normalized Position (vUV.stp)
#define _PC _POS3DC     //  vec3 _PC   = 3D Centered Position in Pixels
#define _PNC _POS3DNC   //  vec3 _PNC  = 3D Normalized + Centered Position
#define _PNR _POS3DNR   //  vec3 _PNR  = 3D Normalized + Ratio Position
#define _PNCR _POS3DNCR //  vec3 _PNCR = 3D Normalized + Centered + Ratio Position

// Shadertoy Inputs
#define iChannel0 sTD2DInputs[0] // sampler2D iChannel0 = First Input Channel (sTD2DInputs[0])
#define iChannel1 sTD2DInputs[1] // sampler2D iChannel1 = Second Input Channel (sTD2DInputs[1])
#define iChannel2 sTD2DInputs[2] // sampler2D iChannel2 = Third Channel (sTD2DInputs[2])
#define iChannel3 sTD2DInputs[3] // sampler2D iChannel3 = Fourth Channel (sTD2DInputs[3])

// TD Compute Shader outputs
#define o0 mTDComputeOutputs[0] // image*D o0 = First Output (mTDComputeOutputs[0])
#define o1 mTDComputeOutputs[1] // image*D o1 = Second Output (mTDComputeOutputs[1])
#define o2 mTDComputeOutputs[2] // image*D o2 = Third Output (mTDComputeOutputs[2])
#define o3 mTDComputeOutputs[3] // image*D o3 = Fourth Output (mTDComputeOutputs[3])
#define o4 mTDComputeOutputs[4] // image*D o4 = Fifth Output (mTDComputeOutputs[4])
#define o5 mTDComputeOutputs[5] // image*D o5 = Sixth Output (mTDComputeOutputs[5])
#define o6 mTDComputeOutputs[6] // image*D o6 = Seventh Output (mTDComputeOutputs[6])
#define o7 mTDComputeOutputs[7] // image*D o7 = Eighth Output (mTDComputeOutputs[7])

// 2D Inputs
#define i0_2D sTD2DInputs[0] // sampler2D i0_2D = First 2D Input Channel (sTD2DInputs[0])
#define i1_2D sTD2DInputs[1] // sampler2D i1_2D = Second 2D Input Channel (sTD2DInputs[1])
#define i2_2D sTD2DInputs[2] // sampler2D i2_2D = Third 2D Input Channel (sTD2DInputs[2])
#define i3_2D sTD2DInputs[3] // sampler2D i3_2D = Fourth 2D Input Channel (sTD2DInputs[3])
#define i4_2D sTD2DInputs[4] // sampler2D i4_2D = Fifth 2D Input Channel (sTD2DInputs[4])
#define i5_2D sTD2DInputs[5] // sampler2D i5_2D = Sixth 2D Input Channel (sTD2DInputs[5])
#define i6_2D sTD2DInputs[6] // sampler2D i6_2D = Seventh 2D Input Channel (sTD2DInputs[6])
#define i7_2D sTD2DInputs[7] // sampler2D i7_2D = Eighth 2D Input Channel (sTD2DInputs[7])

// 3D Inputs
#define i0_3D sTD3DInputs[0] // sampler3D i0_3D = First 3D Input Channel (sTD3DInputs[0])
#define i1_3D sTD3DInputs[1] // sampler3D i1_3D = Second 3D Input Channel (sTD3DInputs[1])
#define i2_3D sTD3DInputs[2] // sampler3D i2_3D = Third 3D Input Channel (sTD3DInputs[2])
#define i3_3D sTD3DInputs[3] // sampler3D i3_3D = Fourth 3D Input Channel (sTD3DInputs[3])
#define i4_3D sTD3DInputs[4] // sampler3D i4_3D = Fifth 3D Input Channel (sTD3DInputs[4])
#define i5_3D sTD3DInputs[5] // sampler3D i5_3D = Sixth 3D Input Channel (sTD3DInputs[5])
#define i6_3D sTD3DInputs[6] // sampler3D i6_3D = Seventh 3D Input Channel (sTD3DInputs[6])
#define i7_3D sTD3DInputs[7] // sampler3D i7_3D = Eighth 3D Input Channel (sTD3DInputs[7])

// 2D Array
#define i0_Array sTD2DArrayInputs[0] // sampler2DArray i0_Array = First 2D Array Input Channel (sTD2DArrayInputs[0])
#define i1_Array sTD2DArrayInputs[1] // sampler2DArray i1_Array = Second 2D Array Input Channel (sTD2DArrayInputs[1])
#define i2_Array sTD2DArrayInputs[2] // sampler2DArray i2_Array = Third 2D Array Input Channel (sTD2DArrayInputs[2])
#define i3_Array sTD2DArrayInputs[3] // sampler2DArray i3_Array = Fourth 2D Array Input Channel (sTD2DArrayInputs[3])
#define i4_Array sTD2DArrayInputs[4] // sampler2DArray i4_Array = Fifth 2D Array Input Channel (sTD2DArrayInputs[4])
#define i5_Array sTD2DArrayInputs[5] // sampler2DArray i5_Array = Sixth 2D Array Input Channel (sTD2DArrayInputs[5])
#define i6_Array sTD2DArrayInputs[6] // sampler2DArray i6_Array = Seventh 2D Array Input Channel (sTD2DArrayInputs[6])
#define i7_Array sTD2DArrayInputs[7] // sampler2DArray i7_Array = Eighth 2D Array Input Channel (sTD2DArrayInputs[7])

// Cube
#define i0_Cube sTDCubeInputs[0] // samplerCube i0_Cube = First Cube Input Channel (sTDCubeInputs[0])
#define i1_Cube sTDCubeInputs[1] // samplerCube i1_Cube = Second Cube Input Channel (sTDCubeInputs[1])
#define i2_Cube sTDCubeInputs[2] // samplerCube i2_Cube = Third Cube Input Channel (sTDCubeInputs[2])
#define i3_Cube sTDCubeInputs[3] // samplerCube i3_Cube = Fourth Cube Input Channel (sTDCubeInputs[3])
#define i4_Cube sTDCubeInputs[4] // samplerCube i4_Cube = Fifth Cube Input Channel (sTDCubeInputs[4])
#define i5_Cube sTDCubeInputs[5] // samplerCube i5_Cube = Sixth Cube Input Channel (sTDCubeInputs[5])
#define i6_Cube sTDCubeInputs[6] // samplerCube i6_Cube = Seventh Cube Input Channel (sTDCubeInputs[6])
#define i7_Cube sTDCubeInputs[7] // samplerCube i7_Cube = Eighth Cube Input Channel (sTDCubeInputs[7])

// 2D Inputs shortcuts
#define i0 i0_2D // sampler2D i0 = First 2D Input Channel (sTD2DInputs[0])
#define i1 i1_2D // sampler2D i1 = Second 2D Input Channel (sTD2DInputs[1])
#define i2 i2_2D // sampler2D i2 = Third 2D Input Channel (sTD2DInputs[2])
#define i3 i3_2D // sampler2D i3 = Fourth 2D Input Channel (sTD2DInputs[3])
#define i4 i4_2D // sampler2D i4 = Fifth 2D Input Channel (sTD2DInputs[4])
#define i5 i5_2D // sampler2D i5 = Sixth 2D Input Channel (sTD2DInputs[5])
#define i6 i6_2D // sampler2D i6 = Seventh 2D Input Channel (sTD2DInputs[6])
#define i7 i7_2D // sampler2D i7 = Eighth 2D Input Channel (sTD2DInputs[7])

// Shadertoy IO
#define fragCoord _UV             // vec2 fragCoord   = 2D Position in Pixels

/* Function Macros */
#define fetch(IN,POS,LODORSAMPLE) texelFetch(IN, POS, LODORSAMPLE)  // fetch(sampler*D IN, ivec* POS, int LOD OR int SAMPLE)      => texelFetch(IN, POS, LOD)    => vec*
#define tx(IN,POS,BIAS) texture(IN, POS, BIAS)                      // tx(sampler*D IN, vec* POS, float OR vec* OR float[] bias)  => texture(IN, POS, BIAS)      => float OR vec4
#define store(OUT,POS,VALUE) imageStore(OUT, POS, VALUE)            // store(gimage*D OUT, vec* POS, vec* VALUE)                  => imageStore(OUT, POS, VALUE) => void (image)
#define td(COLOR) TDOutputSwizzle(COLOR)                            // td(vec4 COLOR)                                             => TDOutputSwizzle(COLOR)      => vec4
