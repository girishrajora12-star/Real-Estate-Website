#!/usr/bin/env python3
"""
Extract frames from a video file into /public/assets/frames/
Replaces old frames, extracts high-quality JPEGs, and generates manifest.json.
"""
import os
import sys
import glob
import json
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "public", "assets")
FRAMES_DIR = os.path.join(ASSETS_DIR, "frames")
DIST_FRAMES_DIR = os.path.join(BASE_DIR, "dist", "assets", "frames")

def get_video_info(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration,r_frame_rate,nb_frames",
        "-of", "json", video_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        data = json.loads(res.stdout)
        stream = data["streams"][0]
        width = int(stream.get("width", 1920))
        height = int(stream.get("height", 1080))
        duration = float(stream.get("duration", 0))
        
        rate_str = stream.get("r_frame_rate", "30/1")
        if "/" in rate_str:
            num, den = rate_str.split("/")
            fps = float(num) / float(den) if float(den) != 0 else 30.0
        else:
            fps = float(rate_str)
            
        nb_frames = stream.get("nb_frames")
        total_frames = int(nb_frames) if nb_frames and nb_frames.isdigit() else int(duration * fps)
        return {"width": width, "height": height, "duration": duration, "fps": fps, "total_frames": total_frames}
    except Exception as e:
        print(f"ffprobe note: {e}, falling back to defaults")
        return {"width": 1920, "height": 1080, "duration": 10.0, "fps": 24.0, "total_frames": 240}

def extract_frames(video_path):
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return False
        
    print(f"Found video: {video_path} ({os.path.getsize(video_path)} bytes)")
    info = get_video_info(video_path)
    print(f"Video metadata: {info}")

    # Remove existing frames
    os.makedirs(FRAMES_DIR, exist_ok=True)
    existing_frames = glob.glob(os.path.join(FRAMES_DIR, "frame_*.jpg"))
    print(f"Removing {len(existing_frames)} existing frames in {FRAMES_DIR}...")
    for f in existing_frames:
        try:
            os.remove(f)
        except OSError:
            pass

    # Extract all frames using ffmpeg with high quality
    # Extract at full resolution or normalized 1920x1080 with q:v 2
    output_pattern = os.path.join(FRAMES_DIR, "frame_%04d.jpg")
    print(f"Extracting frames to {output_pattern}...")
    
    # We can extract at original fps or targeted 15-24fps for ultra smooth web scrub
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", "scale=1920:-2:flags=lanczos",
        "-q:v", "2",
        output_pattern
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    extracted_frames = sorted(glob.glob(os.path.join(FRAMES_DIR, "frame_*.jpg")))
    count = len(extracted_frames)
    print(f"Successfully extracted {count} frames!")

    if count == 0:
        print("Warning: No frames were extracted!")
        return False

    # Create manifest.json
    manifest = {
        "video": os.path.basename(video_path),
        "totalFrames": count,
        "duration": info["duration"] if info["duration"] > 0 else (count / info["fps"]),
        "fps": info["fps"],
        "width": info["width"],
        "height": info["height"]
    }
    manifest_path = os.path.join(FRAMES_DIR, "manifest.json")
    with open(manifest_path, "w") as mf:
        json.dump(manifest, mf, indent=2)
    print(f"Wrote manifest: {manifest}")

    # If dist exists, sync to dist as well
    if os.path.exists(os.path.dirname(DIST_FRAMES_DIR)):
        os.makedirs(DIST_FRAMES_DIR, exist_ok=True)
        # copy first 10 frames and manifest
        shutil.copy2(manifest_path, os.path.join(DIST_FRAMES_DIR, "manifest.json"))
        for f in extracted_frames:
            shutil.copy2(f, os.path.join(DIST_FRAMES_DIR, os.path.basename(f)))
        print(f"Synced {count} frames to dist folder.")

    return True

if __name__ == "__main__":
    candidates = [
        sys.argv[1] if len(sys.argv) > 1 else None,
        os.path.join(ASSETS_DIR, "Home Walkthrough Video.mp4"),
        os.path.join(ASSETS_DIR, "Home_Walkthrough_Video.mp4"),
        os.path.join(ASSETS_DIR, "walkthrough.mp4"),
        os.path.join(ASSETS_DIR, "hf_20261016_142815_403ea31a-8a9a-43a4-a7ff-2aa022b64a3f.mp4"),
    ]
    target = None
    for c in candidates:
        if c and os.path.exists(c):
            target = c
            break

    if not target:
        # Search all mp4s in ASSETS_DIR and PUBLIC_DIR
        mp4s = glob.glob(os.path.join(ASSETS_DIR, "*.mp4")) + glob.glob(os.path.join(BASE_DIR, "public", "*.mp4"))
        if mp4s:
            target = mp4s[0]
            print(f"Targeting discovered mp4: {target}")

    if not target:
        target = os.path.join(ASSETS_DIR, "Home Walkthrough Video.mp4")

    success = extract_frames(target)
    sys.exit(0 if success else 1)
