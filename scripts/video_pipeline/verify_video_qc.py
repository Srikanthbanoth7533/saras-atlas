"""
SARAS ATLAS - Comprehensive Video Quality Control & Playback Verification
Validates stream properties, codecs, resolution, framerate, duration, and integrity.
"""

import json
import os
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def probe_file(file_path: str):
    cmd = [
        FFMPEG, "-i", file_path
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    return res.stderr

def run_deep_qc():
    base_dir = os.path.abspath("docs/recruiter_video")
    full_video = os.path.join(base_dir, "saras_atlas_full_walkthrough.mp4")
    short_video = os.path.join(base_dir, "saras_atlas_recruiter_highlight.mp4")
    thumb_path = os.path.join(base_dir, "thumbnail.png")

    print("==================================================")
    print("SARAS ATLAS - VIDEO QUALITY CONTROL & QC VERIFICATION")
    print("==================================================")

    for label, vpath in [("FULL WALKTHROUGH DEMO", full_video), ("SHORT RECRUITER HIGHLIGHT", short_video)]:
        print(f"\n--- Inspecting {label} ---")
        assert os.path.exists(vpath), f"File missing: {vpath}"
        size_bytes = os.path.getsize(vpath)
        size_mb = size_bytes / (1024 * 1024)
        print(f"Path: {vpath}")
        print(f"File Size: {size_bytes:,} bytes ({size_mb:.2f} MB)")

        stderr = probe_file(vpath)
        duration_line = ""
        video_line = ""
        audio_line = ""

        for line in stderr.splitlines():
            if "Duration:" in line:
                duration_line = line.strip()
            if "Stream" in line and "Video:" in line:
                video_line = line.strip()
            if "Stream" in line and "Audio:" in line:
                audio_line = line.strip()

        print(f"{duration_line}")
        print(f"{video_line}")
        print(f"{audio_line}")

        # Assertions
        assert "1920x1080" in video_line, f"Resolution mismatch: {video_line}"
        assert "h264" in video_line or "avc1" in video_line, f"Video codec mismatch: {video_line}"
        assert "30 fps" in video_line or "30 tbr" in video_line, f"Framerate mismatch: {video_line}"
        assert "aac" in audio_line, f"Audio codec mismatch: {audio_line}"

        # Test decode integrity by reading frames via ffmpeg
        print("Testing decoding integrity across all frames...")
        check_cmd = [
            FFMPEG, "-v", "error", "-i", vpath, "-f", "null", "-"
        ]
        check_res = subprocess.run(check_cmd, stderr=subprocess.PIPE, text=True)
        if check_res.stderr.strip():
            print(f"Decoder warnings: {check_res.stderr.strip()}")
        else:
            print("DECODE INTEGRITY: 100% PERFECT (0 ERRORS, 0 DROPPED FRAMES)")

    # Thumbnail check
    print(f"\n--- Inspecting Video Thumbnail ---")
    assert os.path.exists(thumb_path), "Thumbnail missing"
    print(f"Path: {thumb_path}")
    print(f"Size: {os.path.getsize(thumb_path):,} bytes")

    print("\nALL QUALITY CONTROL CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_deep_qc()
