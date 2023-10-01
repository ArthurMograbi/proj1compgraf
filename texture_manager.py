from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from PIL import Image
from appearance import Appearance
from shader import Shader
from state import State


class Texture(Appearance):
    def __init__ (self, varname, filename):
        self.varname = varname
        self.tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        img = Image.open(filename)
        data = np.array(img)
        width, height = img.size
        if (img.mode == "RGB"):
            mode = GL_RGB
        elif (img.mode == "RGBA"):
            mode = GL_RGBA
        else:
            raise RuntimeError("Unsopported image mode")
        if (data.dtype == "uint8"):
            dtype = GL_UNSIGNED_BYTE
        else:
            raise RuntimeError("Unsupported image component type: " + data.dtype)
        glTexImage2D(GL_TEXTURE_2D, 0, mode, width, height, 0, mode, dtype, data)
        glGenerateMipmap(GL_TEXTURE_2D)
        self.width = width
        self.height = height
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)


    def Load(self, st : State):
        shd : Shader = st.GetShader()
        shd.ActiveTexture(self.varname)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        
    def Unload(self, st : State):
        shd : Shader = st.GetShader()
        shd.DeactiveTexture()


