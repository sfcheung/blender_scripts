# Generate the points on the density function.
# Work in progress

import bpy
from scipy.stats import norm
import numpy as np
from bpy.props import StringProperty, IntProperty, BoolProperty, FloatProperty, EnumProperty
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence

def gen_normal_random(seed = 0, 
                      npoints = 50, 
                      nbins = 20, 
                      xmean = 0, 
                      xsd = 1, 
                      zscale = 3, 
                      jointpoints = True,
                      addfaces = True):   
    """Generate random normal data and create a histogram"""
    if seed > 0:
        rs = RandomState(MT19937(SeedSequence(self.seed)))

    n = npoints
    
    x = np.random.normal(xmean, xsd, n)
    print(x)
    x_hist, x_bins = np.histogram(x, bins = nbins, 
                                  density = True)
    x_hist = x_hist * zscale

    vertices_all = list()
    face_vertices = list()
    for i in range(nbins):
        vertices_all.append((x_bins[i],     0, 0))
        vertices_all.append((x_bins[i],     0, x_hist[i]))
        vertices_all.append((x_bins[i + 1], 0, x_hist[i]))
        vertices_all.append((x_bins[i + 1], 0, 0))        
        j = i * 4
        face_vertices.append((j, j + 1, j + 2, j + 3))
        
    n_vertices = len(vertices_all)
    if (jointpoints):
        edges_all = list(zip(range(0, n_vertices - 1), range(1, n_vertices)))
        edges_all += [(j * 4, j * 4 + 3) for j in range(nbins)]
    else:
        edges_all = []
    
    if (addfaces):
        faces_all = face_vertices
    else:
        faces_all = []

    return [x_hist, vertices_all, edges_all, faces_all]     

 
class gen_random_normal(bpy.types.Operator):
    """Add a histogram of random normal data"""
    bl_idname = "object.add_random_normal"
    bl_label = "Add a histogram of random normal data"
    bl_options = {'REGISTER', 'UNDO'}
    
    npoints: IntProperty(
        name = "Number of points",
        default = 100,
        min = 10,
        soft_min = 10,
    )
    xmean: FloatProperty(
        name = "Mean",
        default = 0,
    )
    xsd: FloatProperty(
        name = "Standard deviation",
        default = 1,
        min = 0,
        soft_min = 0,
    )
    xmin: FloatProperty(
        name = "Minimum of X",
        default = -3,
    )
    xmax: FloatProperty(
        name = "Maximum of X",
        default =  3,
    )
    zscale: FloatProperty(
        name = "Scale for Z axis",
        default = 10,
        min = 0,
        soft_min = 0,
    )
    jointpoints: BoolProperty(
        name = "Joint the points",
        default = True,
    )
    seed: IntProperty(
        name = "Random seed",
        default = 0,
        min = 0,
        soft_min = 0,
    )
    nbins: IntProperty(
        name = "Number of bins",
        default = 10,
        min = 2,
        soft_min = 3,
    )
    addfaces: BoolProperty(
        name = "Add faces",
        default = True,
    )
    
    def execute(self, context):   

        x_hist, vertices_all, edges_all, faces_all = gen_normal_random(
                            seed        = self.seed, 
                            npoints     = self.npoints, 
                            nbins       = self.nbins, 
                            xmean       = self.xmean, 
                            xsd         = self.xsd, 
                            zscale      = self.zscale, 
                            jointpoints = self.jointpoints,
                            addfaces    = self.addfaces)       
    
        mesh        = bpy.data.meshes.new("normal_curve")
        object      = bpy.data.objects.new(mesh.name, mesh)
        collection  = bpy.data.collections.get("Collection")
        collection.objects.link(object)
        object.location = bpy.context.scene.cursor.location
        bpy.context.view_layer.objects.active = object
        mesh.from_pydata(vertices_all, edges_all, faces_all)

        return {'FINISHED'}     

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)    
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "npoints")
        col.prop(self, "xmean")
        col.prop(self, "xsd")
        row = layout.row()
        col = layout.column()
        col.prop(self, "nbins")
        col.prop(self, "zscale")
        col.prop(self, "jointpoints")
        col.prop(self, "addfaces")
        col.prop(self, "seed")
            
        
classes = (
    gen_random_normal,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()    
   