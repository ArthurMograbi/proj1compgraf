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
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

    def generate_vertices(self):
        vertices = []
        angle = 2 * math.pi / self.num_segments
        for i in range(self.num_segments):
            x = math.cos(i * angle) * self.radius
            y = math.sin(i * angle) * self.radius
            vertices.extend([x, y])
        return np.array(vertices, dtype='float32')

    def Draw(self, st):
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.coord_buffer)
        glEnableVertexAttribArray(0)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.num_segments)
        glDisableVertexAttribArray(0)