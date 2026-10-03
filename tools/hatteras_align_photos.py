"""
Line up a before/after pair of oblique storm photos for the slider on the Hatteras Storms page.

    python tools/hatteras_align_photos.py

Fits a homography (least squares) to matching points picked by hand in the two photos, warps the 'before'
photo onto the 'after' one, and crops both to the area they share, below the USGS date labels. Writes
<name>_before_aligned.jpg and <name>_after_aligned.jpg next to the originals, and the fit to
assets/hatteras/data/photo_alignment.json. Refuses a pair whose points disagree with the fit by more than
MAX_RESID_PX.

The points are picked by hand because automatic feature matching (SIFT + RANSAC) was tried on 2026-10-03 and was
unstable on these pairs: so much changed in the storm that only about 10 of 40-200 matches agree, and the fit
moved by 20-200 px with the settings. A homography maps one plane, so houses on pilings sit slightly off.

Only Rodanthe (Irene) is aligned. Frisco and Hatteras Village (Isabel) and Pea Island (Irene) were shot from
different flight lines, so no single warp fits both the front and back of the scene; they stay side by side.

Author:  Hannah A. Henry, Coastal Environmental Change Lab,
         University of North Carolina at Chapel Hill
Contact: hahenry@unc.edu
Version: 2026-10-03
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

SITE = Path(__file__).resolve().parents[1]
IMG = SITE / "assets/hatteras/img"
OUT = SITE / "assets/hatteras/data/photo_alignment.json"
QUALITY = 88
MAX_RESID_PX = 25

# name: before, after, crop box in the after photo (x0, y0, x1, y1; None = widest that is all photo),
# and points as ((x, y) in before, (x, y) in after), in pixels of the original files
PAIRS = {
    "irene/rodanthe": {
        "before": "irene/rodanthe_2008.jpg",
        "after": "irene/rodanthe_2011.jpg",
        "crop": (None, 96, None, 560),
        "points": [
            ((225, 118), (220, 151)),  # roof peak of the cottage the USGS arrow points to
            ((125, 125), (90, 150)),   # roof of the house to its left
            ((322, 150), (347, 205)),  # top of the tower house
            ((295, 75), (267, 95)),    # lower-left corner of the tall house behind
            ((85, 55), (12, 60)),      # red-roofed house, top left
            ((465, 45), (465, 75)),    # sand blowout in the shrubs
            ((698, 37), (690, 57)),    # west tip of the pond
            ((650, 282), (652, 357)),  # NC-12, seaward edge
            ((900, 283), (900, 362)),  # NC-12, seaward edge, further east
        ],
    },
}


def homography(src, dst):
    """Least-squares 3x3 H with dst ~ H @ src (direct linear transform, normalised)."""
    def norm(p):
        c, s = p.mean(0), np.sqrt(2) / np.mean(np.linalg.norm(p - p.mean(0), axis=1))
        return np.array([[s, 0, -s * c[0]], [0, s, -s * c[1]], [0, 0, 1]])
    Ts, Td = norm(src), norm(dst)
    s = (Ts @ np.c_[src, np.ones(len(src))].T).T
    d = (Td @ np.c_[dst, np.ones(len(dst))].T).T
    rows = []
    for (x, y, _), (u, v, _) in zip(s, d):
        rows.append([-x, -y, -1, 0, 0, 0, u * x, u * y, u])
        rows.append([0, 0, 0, -x, -y, -1, v * x, v * y, v])
    H = np.linalg.svd(np.array(rows))[2][-1].reshape(3, 3)
    H = np.linalg.inv(Td) @ H @ Ts
    return H / H[2, 2]


def apply(H, p):
    q = (H @ np.c_[p, np.ones(len(p))].T).T
    return q[:, :2] / q[:, 2:]


def warp(img, H, size):
    """Warp img onto the after photo's frame; PIL wants the map from output pixels back to input."""
    Hi = np.linalg.inv(H)
    Hi = Hi / Hi[2, 2]
    return img.transform(size, Image.Transform.PERSPECTIVE, tuple(Hi.ravel()[:8]), Image.Resampling.BICUBIC)


def main():
    record = {}
    for name, p in PAIRS.items():
        A, B = Image.open(IMG / p["before"]).convert("RGB"), Image.open(IMG / p["after"]).convert("RGB")
        src = np.array([a for a, _ in p["points"]], float)
        dst = np.array([b for _, b in p["points"]], float)
        H = homography(src, dst)
        resid = np.linalg.norm(apply(H, src) - dst, axis=1)
        if resid.max() > MAX_RESID_PX:
            raise SystemExit(f"{name}: a point is {resid.max():.1f} px off the fit; check the points")

        warped = warp(A, H, B.size)
        valid = np.array(warp(Image.new("L", A.size, 255), H, B.size)) > 250
        x0, y0, x1, y1 = p["crop"]
        cols = np.where(valid[y0:y1].all(0))[0]
        x0, x1 = (int(cols.min()) if x0 is None else x0), (int(cols.max()) + 1 if x1 is None else x1)
        for img, suffix in ((warped, "before"), (B, "after")):
            img.crop((x0, y0, x1, y1)).save(IMG / f"{name}_{suffix}_aligned.jpg", quality=QUALITY, optimize=True)
        record[name] = {"before": p["before"], "after": p["after"], "homography": np.round(H, 8).tolist(),
                        "points": p["points"], "residual_px": np.round(resid, 1).tolist(), "crop": [x0, y0, x1, y1]}
        print(f"{name}: {len(src)} points, residual median {np.median(resid):.1f} px, max {resid.max():.1f}; "
              f"crop {x0},{y0}-{x1},{y1} ({x1 - x0}x{y1 - y0})")
    OUT.write_text(json.dumps(record, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
