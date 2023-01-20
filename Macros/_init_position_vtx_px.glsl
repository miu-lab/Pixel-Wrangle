/* Position */

#define _POS2D ivec2(vUV.st * uTDOutputInfo.res.zw)                               // ivec2 POS2D = 2D Position in Pixels
#define _POS3D ivec3(vec3(vUV.st * uTDOutputInfo.res.zw, uTDOutputInfo.depth.y )) // ivec3 POS3D = 3D Position in Pixels
