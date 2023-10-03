from OpenGL.GL import *
import glfw
import random as rd

from camera import *
from color import *
from transform import *
from disk import *
from triangle import *
from node import *
from shader import *
from scene import *
from engine import *
from texture_manager import Texture
from square import Square

class AnimRot(Engine):
  def __init__ (self, trf,rate=6):
    self.trf = trf
    self.rate = rate
  def Update (self, dt):
    self.trf.Rotate(self.rate*dt,0,0,-1)

def initialize ():
  # set background color: white 
  glClearColor(0.8,1.0,1.0,1.0)
  # enable depth test 
  glEnable(GL_DEPTH_TEST)

  # create objects
  global camera
  camera = Camera(0,10,0,10)

  trBase = Transform()
  trBase.Translate(5,5,0)

  trSun = Transform()
  trSun.Scale(.75,.75,1)

  texEar = Texture("face", "images/earth.jpg")
  texMer = Texture("face", "images/mercury.png")
  texSun = Texture("face", "images/sun.png")
  texMoon = Texture("face", "images/moon.jpeg")
  texSpc = Texture("face", "images/space.jpg")

  sun = Node(trf=trSun,apps=[texSun],shps=[Disk(32)])

  trEarEx = Transform()
  trEarMid = Transform()
  trEarIn = Transform()
  trEarMid.Translate(2.5,2.5,0)
  trEarIn.Scale(0.25, 0.25, 1)

  trMunEx = Transform()
  trMunIn = Transform()
  trMunIn.Translate(.5,.5,0)
  trMunIn.Scale(.1,.1,1)

  earth = Node(trf=trEarEx,nodes=[
            Node(trf=trEarMid,nodes=[
              Node(trf=trEarIn,apps=[texEar],shps=[Disk(32)],),
              Node(trf=trMunEx,nodes=[Node(trf=trMunIn,apps=[texMoon],shps=[Disk(32)])])
            ])
          ])

  trMercuryEx = Transform()
  trMercuryIn = Transform()
  trMercuryIn.Translate(1.5,1.5,0)
  trMercuryIn.Scale(.20,.20,1)

  mercury = Node(trf=trMercuryEx,nodes=[Node(trMercuryIn,apps=[texMer],shps=[Disk(32)])])

  background_transform = Transform()
  background_transform.Scale(5, 5, 1)
  bg_node = Node(trf=background_transform, apps=[texSpc], shps=[Square()])
  base = Node(trf=trBase,nodes=[sun,earth,mercury, bg_node])



  shader = Shader()
  shader.AttachVertexShader("./shaders/vertex.glsl")
  shader.AttachFragmentShader("./shaders/fragment.glsl")
  shader.Link()


  # build scene
  root = Node(shader, nodes = [base])
  global scene 
  scene = Scene(root)
  scene.AddEngine(AnimRot(trSun,4))

  scene.AddEngine(AnimRot(trEarEx,10))
  scene.AddEngine(AnimRot(trEarIn,-15))

  scene.AddEngine(AnimRot(trMercuryEx,13.5))
  scene.AddEngine(AnimRot(trMercuryIn,12))

  scene.AddEngine(AnimRot(trMunEx,30))
  scene.AddEngine(AnimRot(trMunIn,-30.4))



def update (dt):
  scene.Update(dt)

def display ():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
  scene.Render(camera)

def keyboard (win, key, scancode, action, mods):
   if key == glfw.KEY_Q and action == glfw.PRESS:
      glfw.set_window_should_close(win,glfw.TRUE)

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)
    win = glfw.create_window(600, 600, "2D scene", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.set_key_callback(win,keyboard)

    # Make the window's context current
    glfw.make_context_current(win)
    print("OpenGL version: ",glGetString(GL_VERSION))

    initialize()

    # Set the background color of the window
    glClearColor(0.05, 0.05, 0.05, 1.0)

    # Loop until the user closes the window
    t0 = glfw.get_time()
    while not glfw.window_should_close(win):       
        t = glfw.get_time()
        update(t-t0)
        t0 = t

        # Clear the color buffer before rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        display()

        # Swap front and back buffers
        glfw.swap_buffers(win)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()