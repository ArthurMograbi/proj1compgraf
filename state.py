import glm
from OpenGL.GL import *

class State:
  def __init__ (self, camera):
    self.camera = camera
    self.shader = []
    self.stack = [glm.mat4(1.0)]
    glUseProgram(0) # compatibility profile as default

  def PushShader (self, shd):
    self.shader.append(shd)
    shd.UseProgram()

  def PopShader (self):
    self.shader.pop()
    if not self.shader:
      glUseProgram(0)
    else:
      self.shader[-1].UseProgram()
  
  def GetShader (self):
    if not self.shader:
      raise SystemExit("Shader not defined")
    return self.shader[-1]

  def GetCamera (self):
    return self.camera

  def PushMatrix (self):
    self.stack.append(self.GetCurrentMatrix())

  def PopMatrix (self):
    self.stack.pop()

  def LoadMatrix (self, mat):
    self.stack[-1] = mat

  def MultMatrix (self, mat):
    self.stack[-1] = self.stack[-1] * mat

  def GetCurrentMatrix (self):
    return self.stack[-1]

  def LoadMatrices (self):
    # set matrices
    shd = self.GetShader()
    mvp = self.camera.GetProjMatrix() * self.camera.GetViewMatrix() * self.GetCurrentMatrix()
    shd.SetUniform("Mvp",mvp)