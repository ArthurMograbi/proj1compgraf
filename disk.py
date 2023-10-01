from OpenGL.GL import *
from shape import Shape
import numpy as np
import math

class Disk(Shape):
    def __init__(self, num_segments=32, radius=1.0):
        self.num_segments = num_segments
        self.radius = radius
        self.vertices = self.generate_vertices()

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.coord_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.coord_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        # Vertex positions
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4*4, None) # 2 positions + 2 texcoords = 4 floats, 4 bytes each
        glEnableVertexAttribArray(0)
        
        # Texture coordinates
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*4, None) # offset by 2 floats (8 bytes)
        glEnableVertexAttribArray(1)

    def generate_vertices(self):
        vertices = []
        tex_coords = [] 
        angle = 2 * math.pi / self.num_segments

        # Center vertex and its texture coordinate
        vertices.extend([0.0, 0.0])
        tex_coords.extend([0.5, 0.5])

        for i in range(self.num_segments):
            x = math.cos(i * angle) * self.radius
            y = math.sin(i * angle) * self.radius
            vertices.extend([x, y])
            
            u = 0.5 + 0.5 * math.cos(i * angle)
            v = 0.5 + 0.5 * math.sin(i * angle)
            tex_coords.extend([u, v])
        
        # Interleave vertex positions and UV coordinates
        data = []
        for i in range(len(vertices) // 2):
            data.extend([vertices[2 * i], vertices[2 * i + 1], tex_coords[2 * i], tex_coords[2 * i + 1]])

        return np.array(data, dtype='float32')

    def Draw(self, st):
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.coord_buffer)
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.num_segments)
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
