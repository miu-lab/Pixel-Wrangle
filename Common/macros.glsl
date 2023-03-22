/* Pixel Wrangle - FACTORY MACROS */


/* Common Function Macros */

#define td(COLOR) TDOutputSwizzle(COLOR)                                      // td(vec4 COLOR)                                            => TDOutputSwizzle(COLOR)           => vec4

#define tx(IN,POS,BIAS) texture(IN, POS, BIAS)                                // tx(sampler*D IN, vec* POS, float OR vec* OR float[] bias) => texture(IN, POS, BIAS)           => float OR vec4
#define fetch(IN,POS,LOD) texelFetch(IN, POS, LOD)                            // fetch(sampler*D IN, ivec* POS, int  LOD)                  => texelFetch( IN,   POS,   LOD   ) => vec4

#define store(OUT,POS,VALUE) imageStore(OUT, POS, VALUE)                      // store(gimage*D OUT, vec* POS,  vec* VALUE)                => imageStore( OUT,  POS,   VALUE )



/* Context Specific Macros */

/* IF */

#ifdef TD_COMPUTE_SHADER

#extension GL_NV_compute_shader_derivatives:enable

/* Shader Mode is 'Compute' */
#define _MODE true                                                            // int _MODE = Return True (The shader mode is 'Compute')

#define _UV ivec2(gl_GlobalInvocationID.xy)                                   // ivec2 _UV = 2D Position in Pixels /* ivec2(gl_GlobalInvocationID.xy) */
#define _P ivec3(gl_GlobalInvocationID.xyz)                                   // ivec3 _P  = 3D Position in Pixels /* ivec3(gl_GlobalInvocationID.xyz) */

#define write(OUT, VALUE) imageStore(OUT, _UV, td(VALUE))                     // write(gimage*D  OUT, vec* VALUE)            => imageStore(OUT, _UV, td(VALUE))
#define writeP(OUT, POS, VALUE) imageStore(OUT, POS, td(VALUE))               // writeP(gimage*D  OUT ,vec* POS, vec* VALUE) => imageStore(OUT, POS, td(VALUE))

#define read(IN) texelFetch(IN, _UV, 0)                                       // read(sampler*D IN)                          => texelFetch(IN, _UV, 0)   => vec4
#define readP(IN, POS) texelFetch(IN, POS, 0)                                 // readP(sampler*D IN,  vec* POS)              => texelFetch(IN, POS, 0)   => vec4
#define readLOD(IN, POS, LOD) texelFetch(IN, POS, LOD)                        // readLOD(sampler*D IN,  vec* POS, int LOD)   => texelFetch(IN, POS, LOD) => vec4

#define load(IN) imageLoad(IN, _UV)                                           // load(gimage*D IN)                           => imageLoad(IN, _UV, 0)    => vec4
#define loadP(IN, POS) imageLoad(IN, POS)                                     // loadP(gimage*D IN, ivec* POS)               => imageLoad(IN, POS, 0)    => vec4
#define loadArray(IN, POS, SAMPLE) imageLoad(IN, POS, SAMPLE)                 // loadArray(gimage*D IN,  vec* POS,  int LOD) => imageLoad(IN, POS, LOD)  => vec4

#define o0 mTDComputeOutputs[0]                                               // image*D o0 = First Compute Output   (mTDComputeOutputs[0])
#define o1 mTDComputeOutputs[1]                                               // image*D o1 = Second Compute Output  (mTDComputeOutputs[1])
#define o2 mTDComputeOutputs[2]                                               // image*D o2 = Third Compute Output   (mTDComputeOutputs[2])
#define o3 mTDComputeOutputs[3]                                               // image*D o3 = Fourth Compute Output  (mTDComputeOutputs[3])
#define o4 mTDComputeOutputs[4]                                               // image*D o4 = Fifth Compute Output   (mTDComputeOutputs[4])
#define o5 mTDComputeOutputs[5]                                               // image*D o5 = Sixth Compute Output   (mTDComputeOutputs[5])
#define o6 mTDComputeOutputs[6]                                               // image*D o6 = Seventh Compute Output (mTDComputeOutputs[6])
#define o7 mTDComputeOutputs[7]                                               // image*D o7 = Eighth Compute Output  (mTDComputeOutputs[7])

#else
/* ELSE */

/* Shader Mode is 'Vertex/Pixel' */
#define _MODE false                                                           // int _MODE = Return False (The shader mode is 'Vertex/Pixel')

#define _UV ivec2(vUV.st * uTDOutputInfo.res.zw)                              // ivec2 _UV = 2D Position in Pixels /* ivec2(vUV.st * uTDOutputInfo.res.zw) */
#define _P ivec3(vec3(vUV.st * uTDOutputInfo.res.zw, uTDOutputInfo.depth.y )) // ivec3 _P  = 3D Position in Pixels /* ivec3(vec3(vUV.st * uTDOutputInfo.res.zw, uTDOutputInfo.depth.y )) */

#define write(OUT, VALUE) OUT = td(VALUE)                                     // write(OUT, vec* VALUE)                                     => OUT = td(VALUE)
#define writeP(OUT, POS, VALUE) OUT = td(VALUE)                               // writeP(OUT, vec* POS, vec* VALUE)                          => OUT = td(VALUE)

#define read(IN) texture(IN, vUV.st, 0)                                       // read(sampler*D IN)                                         => texture( IN, vUV.st, 0   ) => float OR vec4
#define readP(IN, P) texture(IN, P, 0)                                        // read(sampler*D IN, vec* P)                                 => texture( IN, P,      0   ) => float OR vec4
#define readLOD(IN, P, LOD) texture(IN, P, LOD)                               // read(sampler*D IN, vec* P, float OR vec* OR float[] LOD)   => texture( IN, P,      LOD ) => float OR vec4

#endif
/* END IF */



/* Common Variable Macros */

/* Constants */
#define _PI 3.1415926535897932384626433832795                                 // float _PI     = PI Value (3.14...)
#define _GOLD 1.618033988749894                                               // float _GOLD   = Golden Ratio (1.618...)
#define _E 2.7182818284590452353602874713527                                  // float _E      = Euler Number

/* Screen */
#define _RES vec2(uTDOutputInfo.res.z,uTDOutputInfo.res.w)                    // vec2  _RES     = 2D Resolution in Pixels
#define _PXSIZE vec2(1) / _RES                                                // vec2  _PXSIZE  = Size of 1 pixel 1/Resolution
#define _DEPTH uTDOutputInfo.depth.y                                          // float _DEPTH   = Depth
#define _RATIO2D vec2(max(_RES.x/_RES.y, 1),max(_RES.y/_RES.x, 1))            // vec2  _RATIO2D = Ratio from min axis (min axis == 1, max axis >= 1)

/* 2D Position */
#define _UVN vec2(_UV) / _RES+vec2((min(_RATIO2D, 1)*.5)/_RES)                // vec2 _UVN   = 2D Normalized Position                    /* vUV.st          */
#define _UVC _UV - vec2(_RES/2)                                               // vec2 _UVC   = 2D Centered Position in Pixels
#define _UVNC (vec2(_UV) / _RES - .5)                                         // vec2 _UVNC  = 2D Normalized + Centered Position
#define _UVNR _UVN * _RATIO2D                                                 // vec2 _UVNR  = 2D Normalized + Ratio Position
#define _UVNCR (vec2(_RATIO2D) * vec2(_UVN - .5))                             // vec2 _UVNCR = 2D Normalized + Centered + Ratio Position

/* 3D Position */
#define _PN vec3(_UVN,_DEPTH)                                                 // vec3 _PN   = 3D Normalized Position                     /* vUV.stp          */
#define _PC _P - vec3(vec2(_RES/2), _DEPTH/2)                                 // vec3 _PC   = 3D Centered Position in Pixels
#define _PNC _PN - .5                                                         // vec3 _PNC  = 3D Normalized + Centered Position
#define _PNR _PN * vec3(_RATIO2D, _DEPTH/2)                                   // vec3 _PNC  = 3D Normalized + Ratio Position
#define _PNCR ( vec3(_RATIO2D, _DEPTH/2) * vec3(_PN.x - .5, _PN.y - .5, 1 ) ) // vec3 _PNCR = 3D Normalized + Centered + Ratio Position

/* Inputs Samplers Arrays */
#define i2D    sTD2DInputs                                                    // sampler2D       i2D[]    = Array of 2D Inputs Sampler   /* sTD2DInputs      */
#define i3D    sTD3DInputs                                                    // sampler3D       i3D[]    = Array of 3D Inputs Sampler   /* sTD3DInputs      */
#define iCube  sTDCubeInputs                                                  // samplerCube     iCube[]  = Array of Cube Inputs Sampler /* sTDCubeInputs    */
#define iArray sTD2DArrayInputs                                               // sampler2DArray  iArray[] = Array of Cube Inputs Sampler /* sTD2DArrayInputs */

/* 2D Inputs shortcuts */
#define _i0 sTD2DInputs[0]                                                    // sampler2D i0 = First 2D Input Channel                   /* sTD2DInputs[0] */
#define _i1 sTD2DInputs[1]                                                    // sampler2D i1 = Second 2D Input Channel                  /* sTD2DInputs[1] */
#define _i2 sTD2DInputs[2]                                                    // sampler2D i2 = Third 2D Input Channel                   /* sTD2DInputs[2] */
#define _i3 sTD2DInputs[3]                                                    // sampler2D i3 = Fourth 2D Input Channel                  /* sTD2DInputs[3] */
#define _i4 sTD2DInputs[4]                                                    // sampler2D i4 = Fifth 2D Input Channel                   /* sTD2DInputs[4] */
#define _i5 sTD2DInputs[5]                                                    // sampler2D i5 = Sixth 2D Input Channel                   /* sTD2DInputs[5] */
#define _i6 sTD2DInputs[6]                                                    // sampler2D i6 = Seventh 2D Input Channel                 /* sTD2DInputs[6] */
#define _i7 sTD2DInputs[7]                                                    // sampler2D i7 = Eighth 2D Input Channel                  /* sTD2DInputs[7] */

/* Shadertoy Mapping */
#define fragCoord _UV                                                         // vec2 fragCoord   = 2D Position in Pixels

#define iChannel0 _i0                                                          // sampler2D iChannel0 = First Input Channel               /* sTD2DInputs[0] */
#define iChannel1 _i1                                                          // sampler2D iChannel1 = Second Input Channel              /* sTD2DInputs[1] */
#define iChannel2 _i2                                                          // sampler2D iChannel2 = Third Channel                     /* sTD2DInputs[2] */
#define iChannel3 _i3                                                          // sampler2D iChannel3 = Fourth Channel                    /* sTD2DInputs[3] */
