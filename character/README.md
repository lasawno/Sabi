# Sabi — Character engineering, milestone 01

This first source asset contains two actual 3D eyes and four curved eyelid meshes. Each eyelid has an editable blink morph target. The GLB contains a five-second animation with one 0.3-second blink. It is not an animated photograph.

This is an isolated mechanical study. It does not yet resemble the finished Sabi: head anatomy, fur, eyelid rims, tear line, eye gaze, body, skeleton and skin weights are still pending. Do not substitute this for the production character or publish it as finished gameplay.

## Review

Import Sabi-Eyelid-Study.glb into a glTF-compatible 3D editor and play Blink_Study_01. The viewing direction is along +Y, with Z up. Inspect front and oblique views. Examine eye closure at 1.90 seconds, reopening at 1.97 seconds and fully open at 2.10 seconds.

Acceptance still required: no visible eye leakage at closure; convincing eyelid thickness and curvature; no popping from front or side; timing feels organic. Numerical checks do not prove those visual qualities.

## Rebuild

Run `python build_eye_rig.py`. The script emits the GLB and verification.json using Python's standard library.

## Feature order

1. Eye shells and blink mechanics — initial asset built; visual review pending.
2. Sabi head sculpt and eyelid integration — pending.
3. Eye gaze and subtle asymmetry — pending.
4. Breathing, ears and head controls — pending.
5. Spine, limbs, paws and tail skeleton with skin weights — pending.
6. Run, jump and landing cycles — pending.
7. Fur, mobile performance and gameplay integration — pending.

The reference sheet remains the appearance target. This engineering asset is only the first foundation toward it.
