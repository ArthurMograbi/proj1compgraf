#version 410

layout (location=0) in vec4 vertex;
layout (location=1) in vec2 texcoord; //Adicionar coordenadas de textura

uniform mat4 Mvp;

out data {
  vec2 texcoord;
} v;

// out vec2 TexCoord; // Passar coordenadas de textura para o shader de fragmentos

void main (void)
{
  v.texcoord = texcoord;
  gl_Position = Mvp * vertex;
}
