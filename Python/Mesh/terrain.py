from bge import *
from mathutils import *
from math import *

scene = logic.getCurrentScene()
plane = scene.objects["Plane"]
grid = 300

def build():
	builder = types.KX_MeshBuilder("terrain", scene, ["UV"], ["Color"])
	mat = builder.addSlot(plane.meshes[0].materials[0], 0)

	for y in range(grid):
		for x in range(grid):
			npos = (x / 50, y / 50, 0)
			npos2 = (x / 10, y / 10, 0)
			z = noise.multi_fractal(npos, 1, 1.5, 3, 6) * 3
			pos = (x - grid / 2, y - grid / 2, z)
			fac = (z - 15) + noise.multi_fractal(npos2, 1, 1.5, 3, 0)
			#(z - 15) + noise.noise(npos, 0) * 5
			mat.addVertex(pos, uvs=[(x, y)], colors=[(fac, 0, 0, 0)])

	for x in range(grid - 1):
		for y in range(grid - 1):
			i = x + y * grid
			mat.addIndex([i, i + 1, i + 1 + grid])
			mat.addIndex([i, i + 1 + grid, i + grid])

	mat.recalculateNormals()

	plane.replaceMesh(builder.finish(), True, True)

def main():
	print("Generate")
	build()
