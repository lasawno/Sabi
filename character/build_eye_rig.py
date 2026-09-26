"""Sabi milestone 01: editable 3D eyelid shells with glTF morph animation.
Run with Python 3; no third-party dependencies. Units are meters.
This is a mechanical eye study, not the finished Sabi character.
"""
import json, math, struct
from pathlib import Path
ROOT = Path(__file__).parent
doc = {'asset': {'version':'2.0','generator':'Sabi eye study 01'}, 'scene':0,
       'scenes':[{'nodes':[]}], 'nodes':[], 'meshes':[], 'materials':[],
       'buffers':[], 'bufferViews':[], 'accessors':[], 'animations':[]}
blob=bytearray()
def accessor(values, kind, components, ctype=5126):
    while len(blob)%4: blob.append(0)
    start=len(blob); flat=[v for row in values for v in row]
    blob.extend(struct.pack('<'+('f' if ctype==5126 else 'I')*len(flat), *flat))
    view=len(doc['bufferViews']); doc['bufferViews'].append({'buffer':0,'byteOffset':start,'byteLength':len(blob)-start})
    result={'bufferView':view,'componentType':ctype,'count':len(values),'type':kind}
    if ctype==5126:
        result['min']=[min(r[i] for r in values) for i in range(components)]
        result['max']=[max(r[i] for r in values) for i in range(components)]
    doc['accessors'].append(result); return len(doc['accessors'])-1
def material(name, color, roughness):
    doc['materials'].append({'name':name,'pbrMetallicRoughness':{'baseColorFactor':color,'metallicFactor':0,'roughnessFactor':roughness},'doubleSided':True})
    return len(doc['materials'])-1
brown=material('Temporary eyelid material — fur pending',[.16,.065,.025,1],.8)
black=material('Dark glossy eye',[.014,.009,.006,1],.12)
def sphere_patch(name, center, radius, start, end, mat, closed=None):
    rows,cols=24,48
    def vertices(bounds):
        out=[]
        for i in range(rows+1):
            t=bounds[0]+(bounds[1]-bounds[0])*i/rows
            for j in range(cols+1):
                p=2*math.pi*j/cols
                out.append([radius*math.sin(t)*math.cos(p),radius*math.sin(t)*math.sin(p),radius*math.cos(t)])
        return out
    pos=vertices((start,end)); normals=[[v/radius for v in row] for row in pos]; idx=[]
    for i in range(rows):
        for j in range(cols):
            a=i*(cols+1)+j; b=a+cols+1
            idx.extend([[a,b,a+1],[a+1,b,b+1]])
    prim={'attributes':{'POSITION':accessor(pos,'VEC3',3),'NORMAL':accessor(normals,'VEC3',3)},'indices':accessor([[x] for tri in idx for x in tri],'SCALAR',1,5125),'material':mat}
    mesh={'name':name,'primitives':[prim]}
    if closed:
        target=vertices(closed)
        delta=[[b-a for a,b in zip(p,q)] for p,q in zip(pos,target)]
        nd=[[x/radius for x in row] for row in delta]
        prim['targets']=[{'POSITION':accessor(delta,'VEC3',3),'NORMAL':accessor(nd,'VEC3',3)}]
        mesh['weights']=[0]; mesh['extras']={'targetNames':['blink']}
    m=len(doc['meshes']);doc['meshes'].append(mesh)
    n=len(doc['nodes']);doc['nodes'].append({'name':name,'mesh':m,'translation':center})
    doc['scenes'][0]['nodes'].append(n)
    return n
lids=[]
for side,x in [('L',-.068),('R',.068)]:
    center=[x,0,0]
    sphere_patch('Eye.'+side,center,.052,0,math.pi,black)
    lids.append(sphere_patch('UpperLid.'+side,center,.0535,0,1.00,brown,(0,math.pi/2+.015)))
    lids.append(sphere_patch('LowerLid.'+side,center,.0538,2.19,math.pi,brown,(math.pi/2-.015,math.pi)))
# Explicit holds, accelerated close, short contact and slower reopen. Loop is 5s.
times=[0,1.8,1.84,1.88,1.90,1.93,1.97,2.03,2.10,5]
weights=[0,0,.22,.78,1,1,.80,.30,0,0]
ti=accessor([[t] for t in times],'SCALAR',1)
wi=accessor([[w] for w in weights],'SCALAR',1)
doc['animations']=[{'name':'Blink_Study_01','samplers':[{'input':ti,'output':wi,'interpolation':'LINEAR'}], 'channels':[{'sampler':0,'target':{'node':n,'path':'weights'}} for n in lids]}]
doc['buffers']=[{'byteLength':len(blob)}]
js=json.dumps(doc,separators=(',',':')).encode(); js+=b' '*((-len(js))%4)
blob.extend(b'\0'*((-len(blob))%4))
out=struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(blob))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(blob),0x004e4942)+blob
(ROOT/'Sabi-Eyelid-Study.glb').write_bytes(out)
# Mechanical checks, separate from the still-required visual review.
assert all(b>a for a,b in zip(times,times[1:]))
assert weights[0]==weights[-1]==0 and max(weights)==1
assert len(lids)==4 and len(doc['animations'][0]['channels'])==4
open_gap=.0535*math.cos(1)-.0538*math.cos(2.19)
closed_gap=.0535*math.cos(math.pi/2+.015)-.0538*math.cos(math.pi/2-.015)
assert open_gap>.05 and closed_gap<0
assert .0535>.052 and .0538>.052
report={'status':'mechanical_checks_passed','eyelid_channels':4,'open_aperture_m':open_gap,'closed_overlap_m':-closed_gap,'minimum_eye_shell_clearance_m':.0015,'blink_duration_seconds':.3,'loop_seconds':5,'visual_review':'pending; no claim of final realism or clip-free facial integration'}
(ROOT/'verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
