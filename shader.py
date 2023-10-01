from OpenGL.GL import *
import glm


class Shader:
  def __init__ (self):
    self.texunit = 0
    self.shaders = []
    self.pid = None

  def AttachVertexShader (self, filename):
    self.shaders.append(create_shader(GL_VERTEX_SHADER,filename))

  def AttachFragmentShader (self, filename):
    text = _readfile(filename)
    self.shaders.append(create_shader(GL_FRAGMENT_SHADER,filename))

  def AttachGeometryShader (self, filename):
    text = _readfile(filename)
    self.shaders.append(create_shader(GL_GEOMETRY_SHADER,filename))

  def AttachTesselationShader (self, control_filename, evaluation_filename):
    text = _readfile(control_filename)
    self.shaders.append(create_shader(GL_TESS_CONTROL_SHADER,control_filename))
    text = _readfile(evaluation_filename)
    self.shaders.append(create_shader(GL_TESS_EVALUATION_SHADER,evaluation_filename))
  
  def Link (self):
    glBindVertexArray(glGenVertexArrays(1))
    self.pid = create_program(*self.shaders)
  
  def UseProgram (self):
    type(self.pid)
    glUseProgram(self.pid)

  def SetUniform (self, varname, x):
    loc = glGetUniformLocation(self.pid,varname)
    tp = type(x)
    if tp == int:
      glUniform1i(loc,x)
    elif tp == float:
      glUniform1f(loc,x)
    elif tp == glm.vec3: 
      glUniform3fv(loc,1,glm.value_ptr(x))
    elif tp == glm.vec4: 
      glUniform4fv(loc,1,glm.value_ptr(x))
    elif tp == glm.mat4x4:
      glUniformMatrix4fv(loc,1,GL_FALSE,glm.value_ptr(x))
    else:
      raise SystemError("Type not supported in Shader.SetUniform: " + tp)
    
  def ActiveTexture (self, varname):

    self.SetUniform(varname,self.texunit)
    glActiveTexture(GL_TEXTURE0+self.texunit)
    self.texunit += 1
  
  def DeactiveTexture (self):
    self.texunit -= 1

  def Load (self, st):
    st.PushShader(self)

  def Unload (self, st):
    st.PopShader()

def create_shader (type, filename):
  id = glCreateShader(type)
  if not id:
    raise RuntimeError("could not create shader")
  text = _readfile(filename)
  glShaderSource(id,text)
  compile_shader(id,filename)
  return id

def compile_shader (id, filename):
  glCompileShader(id)
  if not glGetShaderiv(id,GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(id).decode()
    raise RuntimeError("Compilation error: " + filename + "\n" + error)

def create_program (*argv):
  id = glCreateProgram()
  if not id:
    raise RuntimeError("could not create shader")
  for arg in argv:
     glAttachShader(id,arg) 
  link_program(id)
  return id

def link_program (id):
  glLinkProgram(id)
  if not glGetProgramiv(id, GL_LINK_STATUS):
      error = glGetProgramInfoLog(id).decode()
      raise RuntimeError('Linking error: ' + error)

# read file to a string
def _readfile (filename):
  with open(filename) as f:
    lines = f.readlines()
  return lines