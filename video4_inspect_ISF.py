#!/usr/bin/env python3
# coding: utf-8
#
# Analyze experimental video
#
# STEP 4: Inspect ImageStructureFunction (videofig player)
#

from sys import argv
import os.path
from configparser import ConfigParser

from ddm_toolkit import ImageStructureFunction
from ddm_toolkit.videofig import videofig 



#%% 
# ==============================
# get PROCESSING PARAMETERS
# ==============================
# Read parameter file, default to "video0_test_params.txt"
# if nothing (easier with Spyder)
argc = len(argv)
if argc == 1:
    argfn = "video0_test_params.txt"
elif argc == 2:
    argfn = argv[1]
else:
    raise Exception('invalid number of arguments')
 
params = ConfigParser(interpolation=None)
params.read(argfn)
fnbase, fnext = os.path.splitext(argfn)

# is source file a full ISF or a radially average ISF?
ISFradialaverage = False
try:
    if params['ISFengine']['ISF_radialaverage']=='True':
        ISFradialaverage = True
except KeyError:
    pass
    
assert not ISFradialaverage, "inspect ISF only possible for full ISF (this ISF is radially averaged"

ISF_fpn = fnbase+'_ISF.npz'
img_overdrive = float(params['ISFengine']['ISF_display_overdrive'])
# overdrive parameter (boost ISF display brightness)



#%% load and display ISF

# load image structure function
IA = ImageStructureFunction.fromFile(ISF_fpn)

Ni = IA.ISF.shape[0] 
    
vmx = IA.ISF.max() / img_overdrive # avoid autoscale of colormap

vf_redraw_init=False
vf_redraw_img=None
def vf_redraw(fri, ax):
    global ISFob
    global vmx
    global vf_redraw_init
    global vf_redraw_img
    if not vf_redraw_init:
        vf_redraw_img=ax.imshow(IA.ISF[fri], 
                                vmin = 0.0, vmax = vmx, 
                                origin = 'lower', animated = True)
        vf_redraw_init=True
    else:
        vf_redraw_img.set_array(IA.ISF[fri])

print("[ENTER]: toggle pause/play")
print("[LEFT]/[RIGHT]: scroll frames")
print("[MOUSE]: manipulate time bar")

videofig(Ni, vf_redraw, play_fps=10)


