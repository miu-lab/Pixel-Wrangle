/*

original_author: miu-lab

description: This function retrieves surface normals from a given position.
You can also use a vec2 offset to adjust screen space sampling precision. Default is 8/Resolution
It returns a vec3 that contains normals data.

use:
- getNormal(vec3 p, float d)
- getNormal(vec3 p)

options:
- NSAMPLE_DIST 32/_RES
*/

#ifndef NSAMPLE_DIST
#define NSAMPLE_DIST min(32/_RES.x, 32/_RES.y)
#endif

vec3 getNormal(vec3 position, float d) {

    vec2  k = vec2(1.0, -1.0); // Switch Vector

    return normalize( k.xyy * MAP_FNC( position + k.xyy * d) +
                      k.yyx * MAP_FNC( position + k.yyx * d) +
                      k.yxy * MAP_FNC( position + k.yxy * d) +
                      k.xxx * MAP_FNC( position + k.xxx * d) );
}

vec3 getNormal(vec3 position) {
    float offset = NSAMPLE_DIST;
    return getNormal(position, offset);
}