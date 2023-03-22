/*

original_author: miu-lab


description: This function cast rays using standard raymarching algorithm based on a pre-declared map function.

It will return a RenderData struct that contains :

    - Position                 (vec3  RenderData.position)
    - Normal                   (vec3  RenderData.normal)
    - Signed Distance Field    (float RenderData.distance)

Before usage, you have to declare your map function that contains your SDF stuff above this import.

The default attempted form is :

float getDistance(vec3 pos){
    // Your SDF Functions here...

    return d; // return your resulting SDF
}

Use MAP_FNC to override function name

note: Raymarching algorithm principles, a great interactive example => https://www.shadertoy.com/view/4dKyRz

use:
RenderData render = rayCast( vec3  ro,
                             vec3  rd,
                             float tmin,
                             float tmax,
                             float hitPrecision,
                             int   maxIterations,
                             float quality )

options: 

    - MAP_FNC(Position)    getDistance(POS)
    - NORMAL_FNC(Position) getNormal(POS)

*/

#include "structs/RayHit.glsl"
#include "getNormal.glsl"

#ifndef MAP_FNC
#define MAP_FNC(Position) getDistance(Position)
#endif

#ifndef NORMAL_FNC
#define NORMAL_FNC(Position, Sample_Dist) getNormal(P, Sample_Dist)
#endif

RayHit rayCast(vec3 eye, vec3 direction, float minDistance, float maxDistance, float hitDistance, int maxSteps, float Quality, float normalSmooth) {

	 // Init Position and Normals
    vec3 position = vec3(0.0);
    vec3 normal = vec3(0.0);
    float distance = 0.0;

    // Start marching at the minimum distance
    float distanceFromOrigin = minDistance;

    // For each marching step
    for(int i = 0; i < maxSteps; i++) {

        // Get the current position
        vec3 currentPosition = eye + direction * distanceFromOrigin;

        // Get the distance to the closest surface from the current position and adjust step size by quality factor
        float distanceToClosestSurface = MAP_FNC(currentPosition) * 1 / Quality;

        // March 1 step further using the distance to the closest surface
        distanceFromOrigin += distanceToClosestSurface;

        /* 
           If the distance from the origin is greater than the maximum distance 
           OR
           The distance to the closest surface is less than the hit distance
        */

        // Write Position and Normal
        if(distanceToClosestSurface < hitDistance * .001) {
            position = currentPosition;
            normal = getNormal(position, min(1/_RES.x, 1/_RES.y) * normalSmooth);
            break;
        }

        // Set SDF default empty value
        else if(distanceFromOrigin > maxDistance) {
            distanceFromOrigin = maxDistance;
            break;
        }
    }

    // Return the distance from the origin
    return RayHit(position, normal, distanceFromOrigin);
}
