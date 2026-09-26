"""Build Sabi's first editable full-body sculpt and idle animation in Blender.

Blender 4.5: blender -b --factory-startup --python build_sabi.py
Add -- --render to render the 12-second review to PNG frames.
This is an initial procedural sculpt, not an approved production character.
"""
import bpy
import math
import json
import sys
from pathlib import Path
from mathutils import Vector

OUT = Path(__file__).resolve().parent / 'output'
OUT.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def material(name, rgb, roughness=.65):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*rgb, 1)
    p.inputs['Roughness'].default_value = roughness
    return m

fur = material('Chocolate brown coat', (.105,.039,.018))
muzzle = material('Warm muzzle', (.22,.095,.041))
inner = material('Ear velvet', (.28,.11,.065))
eye = material('Glossy dark eyes', (.009,.005,.003), .12)
nose = material('Soft black nose', (.023,.012,.009), .28)
cloth = material('Charcoal scarf', (.025,.029,.03))
leather = material('Backpack leather', (.045,.027,.016), .45)
gold = material('Brass hardware', (.63,.36,.10), .28)
gold.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value = .7
# Surface microdetail is a first material pass; no claim of groomed fur.
n = fur.node_tree.nodes
noise = n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 150
bump = n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = .18
bump.inputs['Distance'].default_value = .012
fur.node_tree.links.new(noise.outputs['Fac'], bump.inputs['Height'])
fur.node_tree.links.new(bump.outputs['Normal'], n.get('Principled BSDF').inputs['Normal'])

parts = []
def ellipsoid(name, loc, scale, mat, bone=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=24, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    for p in o.data.polygons: p.use_smooth=True
    if bone: parts.append((o,bone))
    return o

def capsule(name, a, b, width, mat, bone):
    a,b=Vector(a),Vector(b)
    o=ellipsoid(name,(a+b)/2,(width,width,(b-a).length/2+width*.3),mat,bone)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
    return o

def ribbon(name, points, radius, mat, bone):
    c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=4
    s=c.splines.new('BEZIER'); s.bezier_points.add(len(points)-1)
    for p,co in zip(s.bezier_points,points):
        p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);c.materials.append(mat)
    bpy.context.view_layer.objects.active=o;o.select_set(True)
    bpy.ops.object.convert(target='MESH');o.select_set(False)
    parts.append((o,bone));return o

# Z up, face toward -Y. Reference proportions remain editable.
ellipsoid('Torso',(0,.04,1.03),(.32,.23,.49),fur,'spine')
ellipsoid('Chest bib',(0,-.163,1.16),(.23,.085,.29),muzzle,'spine')
ellipsoid('Head',(0,-.02,1.81),(.43,.30,.37),fur,'head')
ellipsoid('Cheek.L',(-.25,-.22,1.72),(.20,.14,.16),fur,'head')
ellipsoid('Cheek.R',(.25,-.22,1.72),(.20,.14,.16),fur,'head')
ellipsoid('Muzzle',(0,-.30,1.66),(.21,.19,.13),muzzle,'head')
ellipsoid('Nose',(0,-.473,1.70),(.083,.052,.055),nose,'head')
ribbon('Mouth',[(-.10,-.453,1.625),(0,-.474,1.61),(.10,-.453,1.625)],.007,nose,'head')

for sign,side in [(-1,'L'),(1,'R')]:
    x=sign*.31
    o=ellipsoid('Ear.'+side,(x,0,2.13),(.205,.105,.36),fur,'ear.'+side)
    o.rotation_euler[1]=sign*.30
    o=ellipsoid('Inner ear.'+side,(x,-.083,2.15),(.135,.035,.255),inner,'ear.'+side)
    o.rotation_euler[1]=sign*.30
    ellipsoid('Eye.'+side,(sign*.17,-.285,1.82),(.095,.062,.112),eye,'head')
    capsule('Thigh.'+side,(sign*.18,.035,.79),(sign*.21,.035,.38),.145,fur,'leg.'+side)
    ellipsoid('Foot.'+side,(sign*.21,-.085,.17),(.15,.23,.12),fur,'leg.'+side)
    for toe in range(3):
        ellipsoid('Toe.%s.%s'%(side,toe),(sign*.21+(toe-1)*.065,-.255,.145),(.032,.072,.035),muzzle,'leg.'+side)
    capsule('Upper arm.'+side,(sign*.30,0,1.38),(sign*.43,-.005,1.08),.10,fur,'arm.'+side)
    capsule('Forearm.'+side,(sign*.43,-.005,1.08),(sign*.43,-.095,.86),.086,fur,'forearm.'+side)
    ellipsoid('Paw.'+side,(sign*.43,-.105,.82),(.092,.082,.11),fur,'forearm.'+side)
    ribbon('Shoulder strap.'+side,[(sign*.22,.18,1.40),(sign*.26,-.12,1.40),(sign*.24,-.22,1.19),(sign*.23,-.12,.98)],.026,leather,'spine')
    ellipsoid('Strap buckle.'+side,(sign*.25,-.237,1.25),(.042,.017,.049),gold,'spine')

ellipsoid('Backpack',(0,.295,1.16),(.245,.16,.29),leather,'spine')
ellipsoid('Backpack flap',(0,.395,1.34),(.245,.07,.12),leather,'spine')
ellipsoid('Backpack clasp',(0,.454,1.23),(.045,.025,.055),gold,'spine')
ellipsoid('Scarf collar',(0,0,1.49),(.28,.26,.095),cloth,'spine')
ellipsoid('Scarf bib',(0,-.205,1.40),(.21,.055,.17),cloth,'spine')
# Simple crown relief built as geometry.
for x,h in [(-.065,.04),(0,.07),(.065,.04)]:
    capsule('Crown point',(x,-.267,1.39),(x,-.267,1.39+h),.016,gold,'spine')
ribbon('Crown base',[(-.08,-.267,1.39),(0,-.273,1.38),(.08,-.267,1.39)],.015,gold,'spine')

tail_points=[(0,.17,.77),(0,.46,.70),(0,.78,.78),(0,1.04,.99),(0,1.14,1.20)]
for i,(a,b) in enumerate(zip(tail_points,tail_points[1:])):
    capsule('Tail volume.%d'%i,a,b,[.17,.23,.24,.18][i],fur,'tail.%d'%i)

# Named skeleton and weighted meshes; this blockout uses rigid per-part weights.
# Continuous topology and blended joint weights are a later sculpt/rig gate.
bpy.ops.object.armature_add(location=(0,0,0))
rig=bpy.context.object;rig.name='Sabi_Rig'
bpy.ops.object.mode_set(mode='EDIT');rig.data.edit_bones.remove(rig.data.edit_bones[0])
def bone(name,a,b,parent=None):
    e=rig.data.edit_bones.new(name);e.head=a;e.tail=b
    if parent:e.parent=rig.data.edit_bones[parent]
bone('root',(0,0,.1),(0,0,.7))
bone('spine',(0,0,.7),(0,0,1.5),'root')
bone('head',(0,0,1.5),(0,0,1.95),'spine')
for sign,side in [(-1,'L'),(1,'R')]:
    bone('ear.'+side,(sign*.26,0,1.99),(sign*.4,0,2.4),'head')
    bone('arm.'+side,(sign*.30,0,1.38),(sign*.43,-.005,1.08),'spine')
    bone('forearm.'+side,(sign*.43,-.005,1.08),(sign*.43,-.095,.86),'arm.'+side)
    bone('leg.'+side,(sign*.18,.035,.79),(sign*.21,.035,.2),'root')
for i in range(4):bone('tail.%d'%i,tail_points[i],tail_points[i+1],'root' if i==0 else 'tail.%d'%(i-1))
bpy.ops.object.mode_set(mode='OBJECT')
for o,b in parts:
    g=o.vertex_groups.new(name=b);g.add(list(range(len(o.data.vertices))),1,'REPLACE')
    mod=o.modifiers.new('Sabi skeletal deformation','ARMATURE');mod.object=rig

# Curved eyelids generated as morphable shell patches, not eye scaling.
lids=[]
for sign,side in [(-1,'L'),(1,'R')]:
    for upper in [True,False]:
        def patch(closed):
            start,end=((0,math.pi/2) if upper else (math.pi/2,math.pi)) if closed else ((0,.76) if upper else (2.46,math.pi))
            return [(sign*.17+.098*math.sin(t)*math.cos(p),-.285+.066*math.sin(t)*math.sin(p),1.82+.115*math.cos(t)) for i in range(17) for j in range(33) for t,p in [(start+(end-start)*i/16,2*math.pi*j/32)]]
        vertices=patch(False);faces=[]
        for i in range(16):
            for j in range(32):
                a=i*33+j;faces.append((a,a+1,a+34,a+33))
        mesh=bpy.data.meshes.new('Lid shell');mesh.from_pydata(vertices,[],faces);mesh.update()
        o=bpy.data.objects.new(('Upper' if upper else 'Lower')+' lid.'+side,mesh);bpy.context.collection.objects.link(o)
        mesh.materials.append(fur)
        for p in mesh.polygons:p.use_smooth=True
        o.shape_key_add(name='Basis');key=o.shape_key_add(name='Blink')
        for v,co in zip(key.data,patch(True)):v.co=co
        g=o.vertex_groups.new(name='head');g.add(list(range(len(vertices))),1,'REPLACE')
        o.modifiers.new('Head follow','ARMATURE').object=rig
        lids.append(key)

scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=360;scene.render.fps=30
def pose(name, keys):
    p=rig.pose.bones[name];p.rotation_mode='XYZ'
    for f,rot in keys:p.rotation_euler=rot;p.keyframe_insert(data_path='rotation_euler',frame=f)
pose('head',[(1,(0,0,0)),(65,(0,0,0)),(95,(.04,0,.32)),(135,(.04,0,.32)),(165,(-.02,0,-.30)),(205,(-.02,0,-.30)),(235,(0,0,0)),(360,(0,0,0))])
for side,sign in [('L',1),('R',-1)]:
    pose('ear.'+side,[(1,(0,0,0)),(90,(.06,0,sign*.08)),(150,(0,0,0)),(185,(-.04,0,-sign*.06)),(240,(0,0,0)),(360,(0,0,0))])
for i in range(4):
    pose('tail.%d'%i,[(f,(0,math.sin((f-1)/359*2*math.pi)*.055*(i+1),0)) for f in [1,46,91,136,181,226,271,316,360]])
# Backpack reach is a blocking pose only; contact must be reviewed and refined.
pose('arm.R',[(1,(0,0,0)),(235,(0,0,0)),(267,(-.45,0,-.22)),(290,(-.45,0,-.22)),(325,(0,0,0)),(360,(0,0,0))])
pose('forearm.R',[(1,(0,0,0)),(235,(0,0,0)),(267,(-1.2,0,0)),(290,(-1.1,0,0)),(325,(0,0,0)),(360,(0,0,0))])
for f in range(1,361):
    p=rig.pose.bones['spine'];v=math.sin((f-1)/359*6*math.pi)
    p.scale=(1+.008*v,1+.014*v,1+.005*v);p.keyframe_insert(data_path='scale',frame=f)
for key in lids:
    for center in [48,151,227,334]:
        for offset,value in [(-4,0),(-1,.75),(0,1),(1,1),(3,.55),(6,0)]:
            key.value=value;key.keyframe_insert(data_path='value',frame=center+offset)
    for f in [1,360]:key.value=0;key.keyframe_insert(data_path='value',frame=f)

# Neutral review stage keeps attention on the sculpt and motion.
floor=material('Review ground',(.025,.032,.04))
ellipsoid('Display plinth',(0,.2,-.025),(1.45,1.45,.09),floor)
bpy.ops.object.camera_add(location=(3.5,-6,2.5));cam=bpy.context.object
cam.rotation_euler=(Vector((0,.1,1.25))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=3.4;scene.camera=cam
for loc,power,size in [((-3,-4,5),650,4),((3,-2,3),400,3),((0,3,4),850,2)]:
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size
    o.rotation_euler=(Vector((0,0,1.3))-o.location).to_track_quat('-Z','Y').to_euler()
scene.world.color=(.07,.07,.07)
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/'frames'/'sabi_')
scene.frame_set(1)
assert len(rig.data.bones)==15
assert len(lids)==4
assert all(o.vertex_groups.get(b) for o,b in parts)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Sabi-Character-Blockout.blend'))
(OUT/'build-report.json').write_text(json.dumps({'bones':len(rig.data.bones),'weighted_parts':len(parts),'blink_controls':len(lids),'frames':360,'visual_review':'pending','stage':'procedural full-body blockout; final sculpt, groom and blended joint weights pending'},indent=2))
if '--render' in sys.argv:
    (OUT/'frames').mkdir(exist_ok=True)
    bpy.ops.render.render(animation=True)
