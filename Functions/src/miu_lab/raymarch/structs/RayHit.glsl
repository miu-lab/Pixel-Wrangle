/*

original_author: miu-lab

description: This struct defines the output structure of the Pixel Wrangle default raymarcher ( the rayCast() function )

It contains :

    - Position                 (vec3  Hit.position)
    - Normal                   (vec3  Hit.normal)
    - Signed Distance Field    (float Hit.distance)

*/

struct RayHit {
    vec3  position;
    vec3  normal;
    float distance;
};