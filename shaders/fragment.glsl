#version 410

uniform vec4 color;
uniform sampler2D face;

in data {
    vec2 texcoord;
}   f;
out vec4 outcolor;

void main (void)
{
    outcolor = texture(face, f.texcoord);
}