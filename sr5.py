from sr1c import Bitmap
from textura import Texture

r = Bitmap()
textu = Textura("piedra.bmp")

r.glCreateWindow(1500, 1500)
r.glViewPort(0, 0, 1499, 1499)
r.load2("cubo.obj", (0, 0, 0), (1, 1, 1), textura = textu)
r.glFinish("cubo.bmp")