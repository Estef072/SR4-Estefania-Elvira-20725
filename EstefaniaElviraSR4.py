# Estefania Elvira 
# Ejercicio 4
# Fecha 08/08/22


from gl import Renderer, V3, _color
from obj import Texture

# Dimensiones
width = 960
height = 540

# Instancia del renderer
rend = Renderer(width, height)

modelTexture = Texture("models/model.bmp")

#rend.glLoadModel("models/model.obj", modelTexture, V3(width/2, height/2, 0), V3(200,200,200))
#rend.glTriangle_standard(V2(10,10), V2(190,10), V2(100,190))

# Salida
rend.glFinish("nada.bmp")

