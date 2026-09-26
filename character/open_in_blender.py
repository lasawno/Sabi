"""Import the milestone eye study into Blender for inspection (not final Sabi)."""
from pathlib import Path
import bpy
from mathutils import Vector

root = Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(root / 'Sabi-Eyelid-Study.glb'))
scene = bpy.context.scene
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 150
bpy.ops.object.camera_add(location=(0, -.55, .06))
camera = bpy.context.object
camera.rotation_euler = (Vector((0,0,0))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type = 'ORTHO'
camera.data.ortho_scale = .34
scene.camera = camera
for location, energy, size in [((-.2,-.3,.3),15,.2),((.2,-.1,.1),8,.15)]:
    bpy.ops.object.light_add(type='AREA', location=location)
    lamp = bpy.context.object
    lamp.data.energy = energy
    lamp.data.shape = 'DISK'
    lamp.data.size = size
    lamp.rotation_euler = (-lamp.location).to_track_quat('-Z','Y').to_euler()
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(root / 'Sabi-Eye-Review.blend'))
