/*

original_author: Inigo Quiles

description: Generate Uniform Fog from Color and SDF

use: 
	- float getFog( vec3 inputColor, float distance, vec3 fogColor, float force)

*/
vec3 getFog( vec3  inputColor,      // Input color
             float distance, // Distance from camera
             vec3  fogColor, // Fog Color
             float force)
{
    float fogAmount = 1 - exp( -distance*force );
    return mix( inputColor, fogColor, fogAmount );
}