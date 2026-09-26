# Sabi

Character development for Clever Levels / Dash.

## Current milestone

The `character/` folder contains an editable 3D eye-and-eyelid generator, a Blender review-scene script, a Mac launcher and the development checklist. The generator recreates the GLB locally, so no binary model download is required.

This is an early eye-mechanics study, not the completed Sabi character. Full-body modeling, fur, rigging, natural idle motion and the requested video remain pending. Numerical checks have passed; visual verification in Blender has not yet been completed.

## Open on a Mac

Install Blender for Apple Silicon into Applications. From the repository folder, run:

```bash
bash character/setup-mac.command
```

The launcher generates the GLB, builds a review scene and opens it in Blender. The launcher and review script have passed syntax checks, but have not yet been successfully run in Blender.

## Next deliverable

A viewable standing animation of Sabi breathing, blinking, looking left and right, adjusting his backpack strap and returning smoothly to idle. See [the development checklist](character/DEVELOPMENT.md). Gameplay integration follows character review.
