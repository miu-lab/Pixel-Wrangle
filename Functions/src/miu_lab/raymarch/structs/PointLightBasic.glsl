/*

original_author: miu-lab

description: This struct defines the output structure of a Pixel Wrangle Basic PointLight model

It contains :

    - Position                 (vec3  PointLightBasic.position)
    - Intensity                (float  PointLightBasic.intensity)
    - Diffuse Contribution     (float PointLightBasic.diffContrib)
    - Specular Contribution    (float PointLightBasic.specContrib)

*/

struct PointLightBasic
{
  vec3  position;
  float intensity;
  float diffContrib;
  float specContrib;
};