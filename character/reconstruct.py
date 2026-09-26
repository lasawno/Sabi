"""Reconstruct Sabi from a single reference image using the public TRELLIS.2 demo.
Usage: python character/reconstruct.py path/to/reference.png
Requires: pip install gradio_client
Optional: HF_TOKEN for the user's authenticated quota.
Outputs are candidates, never automatically approved or deployed.
"""
import os
import sys
import json
import shutil
from pathlib import Path
from gradio_client import Client, handle_file

def main():
    source=Path(sys.argv[1]).resolve()
    if not source.is_file():
        raise SystemExit("Reference image not found")
    out=Path("character/output/reconstruction")
    out.mkdir(parents=True,exist_ok=True)
    client=Client("https://microsoft-trellis-2.hf.space",hf_token=os.environ.get("HF_TOKEN"),httpx_kwargs={"timeout":60},verbose=False)
    client.predict(api_name="/start_session")
    processed=client.predict(handle_file(str(source)),api_name="/preprocess_image")
    preview=client.predict(handle_file(processed),seed=42,resolution="512",api_name="/image_to_3d")
    (out/"preview.html").write_text(str(preview))
    (out/"status.json").write_text(json.dumps({"generation":"completed","export":"pending","visual_approval":False},indent=2))
    try:
        result=client.predict(decimation_target=100000,texture_size=2048,api_name="/extract_glb")
        paths=result if isinstance(result,(tuple,list)) else [result]
        candidate=next(Path(p) for p in paths if isinstance(p,str) and Path(p).is_file())
        shutil.copy2(candidate,out/"Sabi-Candidate.glb")
        (out/"status.json").write_text(json.dumps({"generation":"completed","export":"completed","visual_approval":False},indent=2))
        print("Candidate exported. Compare to all four reference views before rigging.")
    except Exception as error:
        (out/"status.json").write_text(json.dumps({"generation":"completed","export":"blocked","reason":str(error),"visual_approval":False},indent=2))
        raise SystemExit("Export blocked; preview and status preserved. "+str(error))
if __name__=="__main__":
    main()
