#!/usr/bin/env python3
"""Extract the project photo archive and write web-sized JPEGs.

Looks for photos.tar.gz (or photos.tar_*.gz) and area51-promo.mp4.
Long edge is capped at 2000px. Aspect ratio is preserved. Nothing is cropped.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH = [
    ROOT / "incoming",
    Path("/workspace/uploads"),
    Path.home() / "uploads",
]

SETS = {
    "cavalry": 21,
    "area-51": 9,
    "saint": 8,
}
ARCHIVE_DIRS = {
    "cavalry": "cavalry/final",
    "area-51": "area51/final",
    "saint": "saint/final",
}


def find_named(suffixes: tuple[str, ...]) -> Path | None:
    roots = [ROOT] + SEARCH
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            name = path.name.lower()
            if any(name.endswith(suffix) or suffix in name for suffix in suffixes):
                return path
    return None


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def optimize_jpeg(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        "scale="
        "'if(gte(iw,ih),min(2000,iw),-2)':"
        "'if(gte(iw,ih),-2,min(2000,ih))':"
        "flags=lanczos"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vf",
            vf,
            "-q:v",
            "3",
            "-map_metadata",
            "0",
            str(dest),
        ]
    )


def main() -> int:
    archive = find_named(("photos.tar.gz", "photos.tar_"))
    if archive is None:
        print("No photos archive found. Place photos.tar.gz in incoming/ and rerun.", file=sys.stderr)
        return 1

    extract_root = ROOT / "incoming" / "extracted"
    if extract_root.exists():
        shutil.rmtree(extract_root)
    extract_root.mkdir(parents=True)
    with tarfile.open(archive, "r:*") as tar:
        tar.extractall(extract_root)

    for slug, count in SETS.items():
        prefix = ARCHIVE_DIRS[slug].split("/")[0]
        folders = [
            p
            for p in extract_root.rglob("final")
            if p.is_dir() and p.parent.name == prefix
        ]
        folder = folders[0] if folders else extract_root / ARCHIVE_DIRS[slug]
        out_dir = ROOT / "images" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        for index in range(1, count + 1):
            name = f"{index:02d}.jpg"
            src = folder / name
            if not src.exists():
                scoped = [
                    p
                    for p in extract_root.rglob(name)
                    if prefix in p.parts
                ]
                src = scoped[0] if scoped else src
            if not src.exists():
                print(f"Missing {slug} {name}", file=sys.stderr)
                continue
            optimize_jpeg(src, out_dir / name)
            print(f"wrote images/{slug}/{name}")

    cover = ROOT / "images" / "cavalry" / "01.jpg"
    if cover.exists():
        og = ROOT / "images" / "og.jpg"
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(cover),
                "-vf",
                "scale='min(1200,iw)':-2:flags=lanczos",
                "-q:v",
                "3",
                str(og),
            ]
        )
        print("wrote images/og.jpg")

    video = find_named(("area51-promo.mp4", "area51-promo_"))
    if video:
        dest = ROOT / "video" / "area51-promo.mp4"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if video.resolve() != dest.resolve():
            shutil.copy2(video, dest)
        print("wrote video/area51-promo.mp4")
    else:
        print("No Area 51 promo video found.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
