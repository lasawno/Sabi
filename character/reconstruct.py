"""Create an unapproved Sabi reconstruction candidate from the selected reference."""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path
from gradio_client import Client, handle_file

def main():
    source = Path(sys.argv[1]).resolve()
    if not source.is_file():
        raise SystemExit("Reference image not found")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    out = Path("character/output/reconstruction") / digest[:12]
    out.mkdir(parents=True, exist_ok=True)
    status = {"reference_sha256": digest, "reference_name": source.name,
              "stage": "connecting", "visual_approval": False}
    def save():
        (out / "status.json").write_text(json.dumps(status, indent=2))
    save()
    try:
        client = Client("https://microsoft-trellis-2.hf.space",
                        hf_token=os.environ.get("HF_TOKEN"),
                        httpx_kwargs={"timeout": 60}, verbose=False)
        client.predict(api_name="/start_session")
        status["stage"] = "preprocessing"
        save()
        processed = client.predict(handle_file(str(source)), api_name="/preprocess_image")
        status["stage"] = "generating"
        save()
        preview = client.predict(handle_file(processed), seed=42, resolution="512",
                                 api_name="/image_to_3d")
        (out / "preview.html").write_text(str(preview))
        status["stage"] = "exporting"
        save()
        result = client.predict(decimation_target=100000, texture_size=2048,
                                api_name="/extract_glb")
        paths = result if isinstance(result, (tuple, list)) else [result]
        candidate = next((Path(p) for p in paths if isinstance(p, str)
                          and Path(p).is_file() and Path(p).suffix.lower() == ".glb"), None)
        if candidate is None:
            raise RuntimeError("No GLB model returned by export")
        with candidate.open("rb") as stream:
            if stream.read(4) != b"glTF":
                raise RuntimeError("Export is not a valid GLB container")
        shutil.copy2(candidate, out / "Sabi-Candidate.glb")
        status["stage"] = "exported"
        save()
        print("Candidate exported; visual review and rigging are still required.")
    except Exception as error:
        status["failed_stage"] = status["stage"]
        status["stage"] = "blocked"
        status["reason"] = str(error)
        save()
        raise SystemExit("Reconstruction blocked: " + str(error))

if __name__ == "__main__":
    main()
