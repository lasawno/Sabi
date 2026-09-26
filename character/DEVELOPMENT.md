# Sabi development handoff

Repository: `lasawno/Sabi`. Visibility at initial setup: public.

## Current state
Only the isolated eye mechanism is built. The complete Sabi mesh, fur, skeleton, backpack interaction and display video are NOT complete. Numerical checks passed; visual review is pending. Blender 4.5.0 Linux crashed in the hosted environment. The Mac launcher and scene setup are syntax-checked but have not been executed in Blender.

## Mac setup
Install Blender for Apple Silicon from blender.org. From this folder run `bash setup-mac.command`. It rebuilds the GLB, imports it into a clean Blender scene, saves a review scene and opens Blender. This affects only the new scene, not any existing Blender project.

## First finished deliverable
A viewable idle-loop video showing recognizable Sabi standing in a forest-and-stone display setting: breathing, blinking, looking left/right, reaching for a backpack strap and settling back to the starting pose. Build and review each motion individually before combining. Do not substitute a sliding still image or call the eye study finished Sabi.

## Acceptance gates
Match the supplied character reference. Check eyelid closure and oblique views, planted paws, shoulder and wrist deformation, hand-to-strap contact, ear/tail follow-through and loop continuity. Save actual rendered evidence before claiming visual verification. Keep gameplay integration for after character approval.
