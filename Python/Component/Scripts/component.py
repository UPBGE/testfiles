import bge
import sys
import mathutils
import logging
from collections import OrderedDict

class Cursor(bge.types.KX_PythonComponent):
    '''The Player'''
    args = OrderedDict([
        ('MouseHitProp',''),
        ('Offset', 0.1),
    ])
    def start(self, args):
        self.prop = args['MouseHitProp']
        self.offset = args['Offset']

    def update(self):
        active_camera = self.object.scene.active_camera
        x, y = bge.logic.mouse.position
        vect = active_camera.getScreenVect(x, y)
        pos = active_camera.worldPosition
        obj, hit_pos, normal = self.object.rayCast(pos-vect, pos, 500, self.prop, 1, True)
        if obj is not None:
            self.object.position = hit_pos + mathutils.Vector([0,0,self.offset])



def run_from_the_same_file(cont):
    print("See, I run!")
    print(sys.path)
