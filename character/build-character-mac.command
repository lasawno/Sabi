#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
BLENDER_EXECUTABLE="${BLENDER_EXECUTABLE:-/Applications/Blender.app/Contents/MacOS/Blender}"
if [ ! -x "$BLENDER_EXECUTABLE" ]; then
  echo "Install Blender for Apple Silicon into Applications first."
  exit 1
fi
"$BLENDER_EXECUTABLE" --background --factory-startup --python build_sabi.py
"$BLENDER_EXECUTABLE" output/Sabi-Character-Blockout.blend
