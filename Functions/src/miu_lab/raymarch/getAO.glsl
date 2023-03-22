/*

original_author: Inigo Quiles

description: Compute AO from Position and Normals

use: 
	- float raymarchAO( vec3 Position, vec3 Normal, int samples )

*/

#ifndef MAP_FNC
#define MAP_FNC(Position) getDistance(Position)
#endif

float getAO(in vec3 pos, in vec3 nor, int samples) {
  float occ = 0.0;
  float sca = 1.0;
  for(int i = 0; i < samples; i++) {
    float hr = 0.01 + 0.12 * float(i) * 0.2;
    float dd = MAP_FNC(hr * nor + pos);
    occ += (hr - dd) * sca;
    sca *= 0.9;
    if(occ > 0.35)
      break;
  }
  return saturate(1.0 - 3.0 * occ) * (0.5 + 0.5 * nor.y);
}