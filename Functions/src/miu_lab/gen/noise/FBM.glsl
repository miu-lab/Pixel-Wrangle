/*

original_author: Patricio Gonzalez Vivo

description: Generate a Simplex Noise FBM

use: 
	- float sFBM(vec3 p, int octaves, float lacunarity, float gain)
	- vec3  sFBMColor(vec3 p, int octaves, float lacunarity, float gain)

*/

#include "/libs/lygia/generative/snoise_glsl"

float sFBM(vec3 p, int octaves, float lacunarity, float gain) {

	// Initial values
	float val = snoise(p);
	float amp = 0.5;

	// Loop
	for(int i = 0; i < octaves; i++) {
		val += amp * snoise(p);
		p *= lacunarity;
		amp *= gain;
	}
	return val;

}

vec3 sFBMColor(vec3 p, int octaves, float lacunarity, float gain) {

	// Initial values
	vec3 val = snoise3(p);
	float amp = 0.5;

	// Loop
	for(int i = 0; i < octaves; i++) {
		val += amp * snoise3(p);
		p *= lacunarity;
		amp *= gain;
	}
	return val;

}