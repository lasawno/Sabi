# Reconstruction test — 2026-09-26

The rejected procedural full-body generator and its render workflow were removed from the active branch. Historical commits are not approved character assets.

A single-character reference was prepared from the user's approved Sabi reference. TRELLIS.2 public Gradio API connection and preprocessing succeeded. The image_to_3d call completed and returned preview HTML. The extract_glb call was rejected with a ZeroGPU quota error asking for authentication or a wait of approximately 24 hours. No GLB was recovered, and no replacement model has passed visual inspection or been rigged.

The new reconstruct.py preserves preview HTML and status before attempting export. It accepts an optional HF_TOKEN through the environment; no credentials are stored in this repository. Do not launch repeated jobs to evade the service quota. No paid GPU job was started.

Next gate: export the candidate using available authorized quota, inspect all four views against the reference, and only then assess topology, fur and rigging work. Generation success is not evidence of visual fidelity.
