/*

original_author:  Inigo Quiles

description: calculate soft shadows http://iquilezles.org/www/articles/rmshadows/rmshadows.htm

use: float raymarchSoftshadow( vec3 ro, vec3 rd, float tmin, float tmax )

*/

#ifndef MAP_FNC
#define MAP_FNC(Position) getDistance(Position)
#endif

float getSoftShadow( vec3 ro, vec3 rd, in float tmin, in float tmax, float k, float q ) {
    float res = 1.0;
    float t = tmin;
    float ph = 1e20;
    for (int i = 0; i < 3000; i++) {
        float h = MAP_FNC(ro + rd * t);

        if (t > tmax)
            break;

        else if (h < 0.001) {
            res = 0.0;
            break;
        }

        float y = h*h/(2.0*ph);
        float d = sqrt(h*h-y*y);
        res = min( res, k*d/max(0.0,t-y) );
        ph = h;
        t += h * 1/q;
    }
    return res;
}