#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
BLENDER_EXECUTABLE="${BLENDER_EXECUTABLE:-/Applications/Blender.app/Contents/MacOS/Blender}"
if [ ! -x "$BLENDER_EXECUTABLE" ]; then
  echo "Install Blender from https://www.blender.org/download/ into Applications first."
  exit 1
fi
python3 build_eye_rig.py
"$BLENDER_EXECUTABLE" --background --factory-startup --python open_in_blender.py
"$BLENDER_EXECUTABLE" Sabi-Eye-Review.blend
